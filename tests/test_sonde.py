import pytest
import os
import xarray as xr
from halodrops.processor import Sonde

s_id = "test_this_id"
launch_time = "2020-02-02 20:22:02"
file_name_nolaunch = "test_file_nolaunch"
file_name_launch = "test_file_launch"
postaspenfile_name = f"D{file_name_launch[1:]}QC.nc"


def test_Sonde_attrs():
    TestSonde_nolaunchtime = Sonde(s_id)
    TestSonde_withlaunchtime = Sonde(s_id, launch_time=launch_time)

    assert TestSonde_nolaunchtime.serial_id == s_id
    assert TestSonde_nolaunchtime.launch_time is None
    assert TestSonde_withlaunchtime.serial_id == s_id
    assert TestSonde_withlaunchtime.launch_time == launch_time


@pytest.fixture
def tmp_data_directory(tmp_path):
    """
    Create a temporary directory for testing.
    """
    data_directory = tmp_path / "data"
    data_directory.mkdir()
    return str(data_directory)


@pytest.fixture
def temp_afile_dir(tmp_data_directory):
    """
    Create a temporary A-file directory for testing.
    """
    afile_dir = os.path.join(tmp_data_directory, "Level_0")
    os.mkdir(afile_dir)
    return str(afile_dir)


@pytest.fixture
def temp_afile_nolaunchdetected(temp_afile_dir):
    """
    Create a temporary A-file for testing.
    """
    afile = os.path.join(temp_afile_dir, file_name_nolaunch)
    with open(afile, "w") as f:
        f.write("This is a temporary A-file.\nLaunch Obs Done? = 0")
    return str(afile)


@pytest.fixture
def temp_afile_launchdetected(temp_afile_dir):
    """
    Create a temporary A-file for testing.
    """
    afile = os.path.join(temp_afile_dir, file_name_launch)
    with open(afile, "w") as f:
        f.write("This is a temporary A-file.\nLaunch Obs Done? = 1")
    return str(afile)


@pytest.fixture
def temp_postaspenfile(tmp_data_directory):
    """
    Create a temporary post-ASPEN file for testing.
    """
    postaspenfile_dir = os.path.join(tmp_data_directory, "Level_1")
    os.mkdir(postaspenfile_dir)
    postaspenfile = os.path.join(postaspenfile_dir, postaspenfile_name)
    ds = xr.Dataset(dict(foo=("bar", [4, 2])))
    ds.attrs["SondeId"] = s_id
    ds.to_netcdf(postaspenfile)
    return str(postaspenfile)


def test_sonde_add_afile(temp_afile_launchdetected, temp_afile_nolaunchdetected):
    """
    Test the addition of an A-file.
    """
    sonde = Sonde(serial_id=s_id)
    sonde.add_afile(temp_afile_launchdetected)
    assert sonde.afile == temp_afile_launchdetected
    sonde.add_afile(temp_afile_nolaunchdetected)
    assert sonde.afile == temp_afile_nolaunchdetected


def test_sonde_add_postaspenfile_without_launch(temp_afile_nolaunchdetected):
    """
    Test the addition of a post-ASPEN file when a launch has not been detected.
    """
    sonde = Sonde(serial_id=s_id)
    sonde.add_afile(temp_afile_nolaunchdetected)
    sonde.add_path_structure()
    with pytest.raises(ValueError):
        sonde.add_postaspenfile()


def test_sonde_add_postaspenfile_with_only_afile(
    temp_afile_launchdetected, temp_postaspenfile
):
    """
    Test the addition of a post-ASPEN file when an A-file has been added.
    """
    sonde = Sonde(serial_id=s_id)
    sonde.add_afile(temp_afile_launchdetected)
    sonde.add_path_structure()
    sonde.run_aspen()
    assert sonde.postaspenfile == temp_postaspenfile


def test_sonde_add_aspen_ds(temp_afile_launchdetected, temp_postaspenfile):
    """
    Test the addition of an ASPEN dataset.
    """
    sonde = Sonde(serial_id=s_id)
    sonde.add_afile(temp_afile_launchdetected)
    sonde.run_aspen(temp_postaspenfile)
    sonde.add_aspen_ds()
    assert isinstance(sonde.aspen_ds, xr.Dataset)
    assert sonde.aspen_ds.attrs["SondeId"] == s_id


def test_sonde_add_aspen_ds_with_mismatched_sonde_id(
    temp_afile_launchdetected, temp_postaspenfile
):
    """
    Test the addition of an ASPEN dataset with a mismatched SondeId.
    """
    sonde = Sonde(serial_id=s_id[:-1])
    sonde.add_afile(temp_afile_launchdetected)
    sonde.run_aspen(temp_postaspenfile)
    with pytest.raises(ValueError):
        sonde.add_aspen_ds()
