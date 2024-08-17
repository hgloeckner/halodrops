import glob
import logging
from pathlib import Path as pp
from typing import Dict
import os.path

from halodrops.helper import rawreader as rr
from halodrops.processor import Sonde

# create logger
module_logger = logging.getLogger("halodrops.helper.paths")


class Platform:
    """
    Deriving flight paths from the provided platform directory

    The input should align in terms of hierarchy and nomenclature
    with the {doc}`Directory Structure </handbook/directory_structure>` that `halodrops` expects.
    """

    def __init__(
        self,
        data_directory,
        platform_id,
        platform_directory_name=None,
        path_structure="{platform}/Level_0",
    ) -> None:
        self.platform_id = platform_id
        self.platform_directory_name = platform_directory_name
        self.data_directory = data_directory
        self.path_structure = path_structure
        self.flight_ids = self.get_flight_ids()

    def get_flight_ids(self):
        """Returns a list of flight IDs for the given platform and level directory"""
        if self.platform_directory_name is None:
            platform_dir = os.path.join(self.data_directory, self.platform_id)
        else:
            platform_dir = os.path.join(
                self.data_directory, self.platform_directory_name
            )
        flight_ids = []

        dir_with_flights = self.path_structure.format(platform=platform_dir)
        print(dir_with_flights)
        for flight_id in os.listdir(dir_with_flights):
            if os.path.isdir(os.path.join(dir_with_flights, flight_id)):
                flight_ids.append(flight_id)
        return flight_ids


class Flight:
    """
    Deriving paths from the provided directory

    The input should align in terms of hierarchy and nomenclature
    with the {doc}`Directory Structure </handbook/directory_structure>` that `halodrops` expects.
    """

    def __init__(
        self,
        data_directory,
        flight_id,
        platform_id,
        path_structure="{platform}/Level_0/{flight}",
    ):
        """Creates an instance of Paths object for a given flight

        Parameters
        ----------
        `data_directory` : `str`
            Main data directory

        `flight_id` : `str`
            Individual flight directory name

        `platform_id` : `str`
            Platform name

        Attributes
        ----------
        `flight_idpath`
            Path to flight data directory

        `flight_id`
            Name of flight data directory

        `l1dir`
            Path to Level-1 data directory
        """

        self.path_structure = path_structure
        self.data_directory = data_directory

        self.logger = logging.getLogger("halodrops.helper.paths.Paths")

        self.flight_id = flight_id
        self.platform_id = platform_id
        flight_dir = os.path.join(
            self.data_directory,
            self.path_structure.format(
                platform=self.platform_id, flight=self.flight_id
            ),
        )
        self.flight_idpath = flight_dir
        self.l0_dir = flight_dir
        self.l1_dir = flight_dir.replace("Level_0", "Level_1")
        self.l2_dir = flight_dir.replace("Level_0", "Level_2")

        self.logger.info(
            f"Created Path Instance: {self.flight_idpath=}; {self.flight_id=}; {self.l1_dir=}"
        )

    def get_all_afiles(self):
        """Returns a list of paths to all A-files for the given directory
        and also sets it as attribute named 'afiles_list'
        """
        a_files = glob.glob(os.path.join(self.l0_dir, "A*"))
        self.afiles_list = a_files
        return a_files

    def quicklooks_path(self):
        """Path to quicklooks directory

        Function checks for an existing quicklooks directory, and if not found, creates one.

        Returns
        -------
        `str`
            Path to quicklooks directory
        """
        quicklooks_path_str = self.l0_dir.replace("Level_0", "Quicklooks")

        if pp(quicklooks_path_str).exists():
            self.logger.info(f"Path exists: {quicklooks_path_str=}")
        else:
            pp(quicklooks_path_str).mkdir(parents=True)
            self.logger.info(
                f"Path did not exist. Created directory: {quicklooks_path_str=}"
            )
        return quicklooks_path_str

    def populate_sonde_instances(self) -> Dict:
        """Returns a dictionary of `Sonde` class instances for all A-files found in `flight_idpath`
        and also sets the dictionary as value of `Sondes` attribute
        """
        afiles = self.get_all_afiles()

        Sondes = {}

        for a_file in afiles:
            launch_detect = rr.check_launch_detect_in_afile(a_file)
            sonde_id = rr.get_sonde_id(a_file)
            launch_time = rr.get_launch_time(a_file)
            Sondes[sonde_id] = Sonde(sonde_id, launch_time=launch_time)
            Sondes[sonde_id].add_launch_detect(launch_detect)
            Sondes[sonde_id].add_flight_id(self.flight_id)
            Sondes[sonde_id].add_platform_id(self.platform_id)
            Sondes[sonde_id].add_afile(a_file)
            Sondes[sonde_id].add_level_dir()

        object.__setattr__(self, "Sondes", Sondes)

        return Sondes
