import pytest
import os
import xarray as xr
from halodrops.processor import Gridded

sondes = None
flight_id = "20240811"
platform_id = "HALO"
l3_default = f"{platform_id}_{flight_id}_Level_3.nc"
l3_template = "{flight_id}_{platform}_Level_3.nc"


@pytest.fixture
def gridded():
    return Gridded(sondes, flight_id=flight_id, platform_id=platform_id)


def test_l3_dir(gridded):
    with pytest.raises(ValueError):
        gridded.get_l3_dir()


def test_l3_dir_name(gridded):
    gridded.get_l3_dir(l3_dirname="test")
    assert gridded.l3_dir == "test"


def test_l3_default(gridded):
    gridded.get_l3_filename()
    assert gridded.l3_filename == l3_default


def test_l3_template(gridded):
    gridded.get_l3_filename(l3_filename_template=l3_template)
    assert gridded.l3_filename == l3_template.format(
        flight_id=flight_id, platform=platform_id
    )
