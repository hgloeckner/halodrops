from halodrops.helper import paths
import os

main_data_directory = "../sample"
platform = "HALO"
flightdate = "20200101"
path_structure = "levels_first"

if path_structure == "levels_first":
    l1_path = os.path.join(main_data_directory, platform, "Level_1", flightdate)
if path_structure == "flightid_first":
    l1_path = os.path.join(main_data_directory, platform, flightdate, "Level_1")
    
quicklooks_path = os.path.join(main_data_directory, platform, flightdate, "Quicklooks")

object = paths.Flight(main_data_directory, flightdate, platform)


def test_l1_path():
    assert object.l1dir == l1_path


def test_quicklooks_path():
    assert object.quicklooks_path() == quicklooks_path
