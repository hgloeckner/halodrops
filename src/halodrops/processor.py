import ast
from dataclasses import dataclass, field, KW_ONLY
from datetime import datetime
from typing import Any, Optional, List
import os
import subprocess
import warnings

import numpy as np
import xarray as xr


from halodrops.helper import rawreader as rr
import halodrops.helper as hh

_no_default = object()


@dataclass(order=True, frozen=True)
class Sonde:
    """Class identifying a sonde and containing its metadata

    A `Sonde` identifies an instrument that has been deployed. This means that pre-initialization sondes do not exist for this class.

    Every `Sonde` mandatorily has a `serial_id` which is unique. Therefore, all instances with the same `serial_id` are to be considered as having the same metadata and data.

    Optionally, the `sonde` also has metadata attributes, which can be broadly classified into:

    - campaign and flight information
    - location and time information of launch
    - performance of the instrument and sensors
    - other information such as reconditioning status, signal strength, etc.
    """

    sort_index: np.datetime64 = field(init=False, repr=False)
    serial_id: str
    _: KW_ONLY
    launch_time: Optional[Any] = None

    def __post_init__(self):
        """
        Initializes the 'qc' attribute as an empty object and sets the 'sort_index' attribute based on 'launch_time'.

        The 'sort_index' attribute is only applicable when 'launch_time' is available. If 'launch_time' is None, 'sort_index' will not be set.
        """
        object.__setattr__(self, "qc", type("", (), {})())
        if self.launch_time is not None:
            object.__setattr__(self, "sort_index", self.launch_time)

    def add_flight_id(self, flight_id: str) -> None:
        """Sets attribute of flight ID

        Parameters
        ----------
        flight_id : str
            The flight ID of the flight during which the sonde was launched
        """
        object.__setattr__(self, "flight_id", flight_id)

    def add_platform_id(self, platform_id: str) -> None:
        """Sets attribute of platform ID

        Parameters
        ----------
        platform_id : str
            The platform ID of the flight during which the sonde was launched
        """
        object.__setattr__(self, "platform_id", platform_id)

    def add_spatial_coordinates_at_launch(self, launch_coordinates: List) -> None:
        """Sets attributes of spatial coordinates at launch

        Expected units for altitude, latitude and longitude are
        meter above sea level, degree north and degree east, respectively.

        Parameters
        ----------
        launch_coordinates : List
            List must be provided in the order of [`launch_alt`,`launch_lat`,`launch_lon`]
        """
        try:
            launch_alt, launch_lat, launch_lon = launch_coordinates
            object.__setattr__(self, "launch_alt", launch_alt)
            object.__setattr__(self, "launch_lat", launch_lat)
            object.__setattr__(self, "launch_lon", launch_lon)
        except:
            print(
                "Check if the sonde detected a launch, otherwise launch coordinates cannot be set"
            )

    def add_launch_detect(self, launch_detect_bool: bool) -> None:
        """Sets bool attribute of whether launch was detected

        Parameters
        ----------
        launch_detect_bool : bool
            True if launch detected, else False
        """
        object.__setattr__(self, "launch_detect", launch_detect_bool)

    def add_afile(self, path_to_afile: str) -> None:
        """Sets attribute with path to A-file of the sonde

        Parameters
        ----------
        path_to_afile : str
            Path to the sonde's A-file
        """
        object.__setattr__(self, "afile", path_to_afile)
        return self

    def add_level_dir(self):
        if not hasattr(self, "afile"):
            raise ValueError("No afile in sonde. Cannot continue")
        l0_dir = os.path.dirname(self.afile)
        l1_dir = l0_dir.replace("Level_0", "Level_1")
        l2_dir = l0_dir.replace("Level_0", "Level_2")
        l3_dir = l0_dir.replace("Level_0", "Level_3")

        object.__setattr__(self, "l0_dir", l0_dir)
        object.__setattr__(self, "l1_dir", l1_dir)
        object.__setattr__(self, "l2_dir", l2_dir)
        object.__setattr__(self, "l3_dir", l3_dir)

    def run_aspen(self, path_to_postaspenfile: str = None) -> None:
        """Runs aspen and sets attribute with path to post-ASPEN file of the sonde

        If the A-file path is known for the sonde, i.e. if the attribute `path_to_afile` exists,
        then the function will attempt to look for a post-ASPEN file of the same date-time as in the A-file's name.
        Sometimes, the post-ASPEN file might not exist (e.g. because launch was not detected), and in
        such cases, ASPEN will run in a docker image and create the file.

        If the A-file path is not known for the sonde, the function will expect the argument
        `path_to_postaspenfile` to be not empty.

        Parameters
        ----------
        path_to_postaspenfile : str, optional
            The path to the post-ASPEN file. If not provided, the function will attempt to construct the path from the `afile` attribute.

        Attributes Set
        --------------
        postaspenfile : str
            The path to the post-ASPEN file. This attribute is set if the file exists at the constructed or provided path.
        """

        l0_dir = self.l0_dir  # os.path.dirname(self.afile)
        aname = os.path.basename(self.afile)
        dname = "D" + aname[1:]
        l1_dir = self.l1_dir
        l1_name = dname.split(".")[0] + "QC.nc"

        if path_to_postaspenfile is None:
            path_to_postaspenfile = os.path.join(l1_dir, l1_name)

        if not os.path.exists(path_to_postaspenfile):
            os.makedirs(l1_dir, exist_ok=True)
            subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--mount",
                    f"type=bind,source={l0_dir},target=/input",
                    "--mount",
                    f"type=bind,source={l1_dir},target=/output",
                    "ghcr.io/atmdrops/aspenqc:4.0.2",
                    "-i",
                    f"/input/{dname}",
                    "-n",
                    f"/output/{l1_name}",
                ],
                check=True,
            )

        object.__setattr__(self, "postaspenfile", path_to_postaspenfile)
        return self

    def add_aspen_ds(self) -> None:
        """Sets attribute with an xarray Dataset read from post-ASPEN file

        The function will first check if the serial ID of the instance and that obtained from the
        global attributes of the post-ASPEN file match. If they don't, function will print out an error.

        If the `postaspenfile` attribute doesn't exist, function will print out an error
        """

        if hasattr(self, "postaspenfile"):
            ds = xr.open_dataset(self.postaspenfile)
            if "SondeId" not in ds.attrs:
                if ds.attrs["SoundingDescription"].split(" ")[1] == self.serial_id:
                    object.__setattr__(self, "aspen_ds", ds)
                else:
                    raise ValueError(
                        f"I didn't find the `SondeId` attribute, so checked the `SoundingDescription` attribute. I found the ID in the `SoundingDescription` global attribute ({ds.attrs['SoundingDescription'].split(' ')[1]}) to not match with this instance's `serial_id` attribute ({self.serial_id}). Therefore, I am not storing the xarray dataset as an attribute."
                    )
            elif ds.attrs["SondeId"] == self.serial_id:
                object.__setattr__(self, "aspen_ds", ds)
            else:
                raise ValueError(
                    f"I found the `SondeId` global attribute ({ds.attrs['SondeId']}) to not match with this instance's `serial_id` attribute ({self.serial_id}). Therefore, I am not storing the xarray dataset as an attribute."
                )
        else:
            raise ValueError(
                f"I didn't find the `postaspenfile` attribute for Sonde {self.serial_id}, therefore I can't store the xarray dataset as an attribute"
            )
        return self

    def filter_no_launch_detect(self) -> None:
        """
        Filter out sondes that did not detect a launch

        The function will check if the `launch_detect` attribute exists and if it is False.
        If the attribute doesn't exist, the function will raise an error.
        If the attribute exists and is False, the function will print a no-launch detected message.
        If the attribute exists and is True, the function will return the object.

        This function serves as a checkpoint for filtering out sondes
        that did not detect a launch before running functions
        that will require `aspen_ds`, e.g. the QC functions.

        Parameters
        ----------
        None

        Returns
        -------
        self : Sonde object
            The Sonde object itself, if the launch was detected, else None

        Raises
        ------
        ValueError
            If the `launch_detect` attribute does not exist.
        """
        if hasattr(self, "launch_detect"):
            if self.launch_detect == False:
                print(
                    f"No launch detected for Sonde {self.serial_id}. I am not running QC checks for this Sonde."
                )
            else:
                return self
        else:
            raise ValueError(
                f"The attribute `launch_detect` does not exist for Sonde {self.serial_id}."
            )

    def detect_floater(
        self,
        gpsalt_threshold: float = 25,
        consecutive_time_steps: int = 3,
        skip: bool = False,
    ):
        """
        Detects if a sonde is a floater.

        Parameters
        ----------
        gpsalt_threshold : float, optional
            The gpsalt altitude below which the sonde will check for time periods when gpsalt and pres have not changed. Default is 25.
        skip : bool, optional
            If True, the function will return the object without performing any operations. Default is False.

        Returns
        -------
        self
            The object itself with the new `is_floater` attribute added based on the function parameters.
        """
        if hh.get_bool(skip):
            return self
        else:
            if isinstance(gpsalt_threshold, str):
                gpsalt_threshold = float(gpsalt_threshold)

            if hasattr(self, "aspen_ds"):
                surface_ds = (
                    self.aspen_ds.where(
                        self.aspen_ds.gpsalt < gpsalt_threshold, drop=True
                    )
                    .sortby("time")
                    .dropna(dim="time", how="any", subset=["pres", "gpsalt"])
                )
                gpsalt_diff = np.diff(surface_ds.gpsalt)
                pressure_diff = np.diff(surface_ds.pres)
                gpsalt_diff_below_threshold = (
                    np.abs(gpsalt_diff) < 1
                )  # GPS altitude value at surface shouldn't change by more than 1 m
                pressure_diff_below_threshold = (
                    np.abs(pressure_diff) < 1
                )  # Pressure value at surface shouldn't change by more than 1 hPa
                floater = gpsalt_diff_below_threshold & pressure_diff_below_threshold
                if np.any(floater):
                    object.__setattr__(self, "is_floater", True)
                    for time_index in range(len(floater) - consecutive_time_steps + 1):
                        if np.all(
                            floater[time_index : time_index + consecutive_time_steps]
                        ):
                            landing_time = surface_ds.time[time_index - 1].values
                            object.__setattr__(self, "landing_time", landing_time)
                            print(
                                f"{self.serial_id}: Floater detected! The landing time is estimated as {landing_time}."
                            )
                            break
                        if not hasattr(self, "landing_time"):
                            print(
                                f"{self.serial_id}: Floater detected! However, the landing time could not be estimated. Therefore setting landing time as {surface_ds.time[0].values}"
                            )
                            object.__setattr__(
                                self, "landing_time", surface_ds.time[0].values
                            )
                else:
                    object.__setattr__(self, "is_floater", False)
            else:
                raise ValueError(
                    "The attribute `aspen_ds` does not exist. Please run `add_aspen_ds` method first."
                )
            return self

    def crop_aspen_ds_to_landing_time(self):
        """
        Crops the aspen_ds to the time period before landing.

        Parameters
        ----------
        None

        Returns
        -------
        self
            The object itself with the new `cropped_aspen_ds` attribute added if the sonde is a floater.
        """
        if hasattr(self, "is_floater"):
            if self.is_floater:
                if hasattr(self, "landing_time"):
                    object.__setattr__(
                        self,
                        "cropped_aspen_ds",
                        self.aspen_ds.sel(time=slice(self.landing_time, None)),
                    )
        else:
            raise ValueError(
                "The attribute `is_floater` does not exist. Please run `detect_floater` method first."
            )
        return self

    def profile_fullness(
        self,
        variable_dict={"u_wind": 4, "v_wind": 4, "rh": 2, "tdry": 2, "pres": 2},
        time_dimension="time",
        timestamp_frequency=4,
        fullness_threshold=0.75,
        add_fullness_fraction_attribute=True,
        skip=False,
    ):
        """
        Calculates the profile coverage for a given set of variables, considering their sampling frequency.
        If the sonde is a floater, the function will take the `cropped_aspen_ds` attribute
        (calculated with the `crop_aspen_ds_to_landing_time` method) as the dataset to calculate the profile coverage.

        This function assumes that the time_dimension coordinates are spaced over 0.25 seconds,
        implying a timestamp_frequency of 4 hertz. This is applicable for ASPEN-processed QC and PQC files,
        specifically for RD41.

        For each variable in the variable_dict, the function calculates the fullness fraction. If the fullness
        fraction is less than the fullness_threshold, it sets an attribute in `self.qc` named
        "profile_fullness_{variable}" to False. Otherwise, it sets this attribute to True.

        If add_fullness_fraction_attribute is True, the function also sets an attribute in `self` named
        "profile_fullness_fraction_{variable}" to the calculated fullness fraction.

        Parameters
        ----------
        variable_dict : dict, optional
            Dictionary containing the variables in `self.aspen_ds` and their respective sampling frequencies.
            The function will estimate the weighted profile-coverage for these variables.
            Default is {'u_wind':4,'v_wind':4,'rh':2,'tdry':2,'pres':2}.
        time_dimension : str, optional
            The independent dimension of the profile. Default is "time".
        timestamp_frequency : numeric, optional
            The sampling frequency of `time_dimension` in hertz. Default is 4.
        fullness_threshold : float or str, optional
            The threshold for the fullness fraction. If the calculated fullness fraction is less than this threshold,
            the profile is considered not full. Default is 0.8.
        add_fullness_fraction_attribute : bool or str, optional
            If True, the function will add the fullness fraction as an attribute to the object. Default is True.
            If provided as string, it should be possible to convert it to a boolean value with the helper get_bool function.
        skip : bool, optional
            If True, the function will return the object without performing any operations. Default is False.

        Returns
        -------
        self
            The object itself, possibly with new attributes added based on the function parameters.
        """
        if hh.get_bool(skip):
            return self
        else:
            if isinstance(fullness_threshold, str):
                fullness_threshold = float(fullness_threshold)

            for variable, sampling_frequency in variable_dict.items():
                if self.is_floater:
                    if not hasattr(self, "cropped_aspen_ds"):
                        self.crop_aspen_ds_to_landing_time()
                    dataset = self.cropped_aspen_ds[variable]
                else:
                    dataset = self.aspen_ds[variable]

                weighed_time_size = len(dataset[time_dimension]) / (
                    timestamp_frequency / sampling_frequency
                )
                fullness_fraction = (
                    np.sum(~np.isnan(dataset.values)) / weighed_time_size
                )
                if fullness_fraction < fullness_threshold:
                    object.__setattr__(
                        self.qc,
                        f"profile_fullness_{variable}",
                        False,
                    )
                else:
                    object.__setattr__(
                        self.qc,
                        f"profile_fullness_{variable}",
                        True,
                    )
                if hh.get_bool(add_fullness_fraction_attribute):
                    object.__setattr__(
                        self,
                        f"profile_fullness_fraction_{variable}",
                        fullness_fraction,
                    )
            return self

    def near_surface_coverage(
        self,
        variables=["u_wind", "v_wind", "rh", "tdry", "pres"],
        alt_bounds=[0, 1000],
        alt_dimension_name="alt",
        count_threshold=50,
        add_near_surface_count_attribute=True,
        skip=False,
    ):
        """
        Calculates the fraction of non-null values in specified variables near the surface.

        Parameters
        ----------
        variables : list, optional
            The variables to consider for the calculation. Defaults to ["u_wind","v_wind","rh","tdry","pres"].
        alt_bounds : list, optional
            The lower and upper bounds of altitude in meters to consider for the calculation. Defaults to [0,1000].
        alt_dimension_name : str, optional
            The name of the altitude dimension. Defaults to "alt". If the sonde is a floater, this will be set to "gpsalt" regardless of user-provided value.
        count_threshold : int, optional
            The minimum count of non-null values required for a variable to be considered as having near surface coverage. Defaults to 50.
        add_near_surface_count_attribute : bool, optional
            If True, adds the count of non-null values as an attribute for every variable to the object. Defaults to True.
        skip : bool, optional
            If True, skips the calculation and returns the object as is. Defaults to False.

        Returns
        -------
        self
            The object with updated attributes.

        Raises
        ------
        ValueError
            If the attribute `aspen_ds` does not exist. The `add_aspen_ds` method should be run first.
        """
        if hh.get_bool(skip):
            return self
        else:
            if not hasattr(self, "aspen_ds"):
                raise ValueError(
                    "The attribute `aspen_ds` does not exist. Please run `add_aspen_ds` method first."
                )

            if not hasattr(self, "is_floater"):
                raise ValueError(
                    "The attribute `is_floater` does not exist. Please run `detect_floater` method first."
                )

            if self.is_floater:
                alt_dimension_name = "gpsalt"

            if isinstance(alt_bounds, str):
                alt_bounds = alt_bounds.split(",")
                alt_bounds = [float(alt_bound) for alt_bound in alt_bounds]
            if isinstance(count_threshold, str):
                count_threshold = int(count_threshold)
            if isinstance(variables, str):
                variables = variables.split(",")

            for variable in variables:
                dataset = self.aspen_ds[[variable, alt_dimension_name]]
                near_surface = dataset.where(
                    (dataset[alt_dimension_name] > alt_bounds[0])
                    & (dataset[alt_dimension_name] < alt_bounds[1]),
                    drop=True,
                )

                near_surface_count = np.sum(~np.isnan(near_surface[variable].values))
                if near_surface_count < count_threshold:
                    object.__setattr__(
                        self.qc,
                        f"near_surface_coverage_{variable}",
                        False,
                    )
                else:
                    object.__setattr__(
                        self.qc,
                        f"near_surface_coverage_{variable}",
                        True,
                    )
                if hh.get_bool(add_near_surface_count_attribute):
                    object.__setattr__(
                        self,
                        f"near_surface_count_{variable}",
                        near_surface_count,
                    )
            return self

    def filter_qc_fail(self, filter_flags=None):
        """
        Filters the sonde based on a list of QC flags. If any of the flags are False, the sonde will be filtered out from creating L2.
        If the sonde passes all the QC checks, the attributes listed in filter_flags will be removed from the sonde object.

        Parameters
        ----------
        filter_flags : str or list, optional
            Comma-separated string or list of QC-related attribute names to be checked. Each item can be a specific attribute name or a prefix to include all attributes starting with that prefix. You can also provide 'all_except_<prefix>' to filter all flags except those starting with '<prefix>'. If 'all_except_<prefix>' is provided, it should be the only value in filter_flags. If not provided, no sondes will be filtered.

        Returns
        -------
        self : object
            The sonde object itself, with the attributes listed in filter_flags removed if it passes all the QC checks.

        Raises
        ------
        ValueError
            If a flag in filter_flags does not exist as an attribute of the sonde object, or if 'all_except_<prefix>' is provided in filter_flags along with other values. Please ensure that the flag names provided in 'filter_flags' correspond to existing QC attributes. If you're using a prefix to filter attributes, make sure the prefix is correct. Check your skipped QC functions or your provided list of filter flags.
        """
        all_qc_attributes = [attr for attr in dir(self.qc) if not attr.startswith("__")]

        if filter_flags is None:
            filter_flags = []
        elif isinstance(filter_flags, str):
            filter_flags = filter_flags.split(",")
        elif isinstance(filter_flags, list):
            pass
        else:
            raise ValueError(
                "Invalid type for filter_flags. It must be one of the following:\n"
                "- None: If you want to filter against all QC attributes.\n"
                "- A string: If you want to provide a comma-separated list of individual flag values or prefixes of flag values.\n"
                "- A list: If you want to provide individual flag values or prefixes of flag values."
            )

        if (
            any(flag.startswith("all_except_") for flag in filter_flags)
            and len(filter_flags) > 1
        ):
            raise ValueError(
                "If 'all_except_<prefix>' is provided in filter_flags, it should be the only value."
            )

        new_filter_flags = []
        for flag in filter_flags:
            if flag.startswith("all_except_"):
                prefix = flag.replace("all_except_", "")
                new_filter_flags.extend(
                    [attr for attr in all_qc_attributes if not attr.startswith(prefix)]
                )
            else:
                new_filter_flags.extend(
                    [attr for attr in all_qc_attributes if attr.startswith(flag)]
                )

        filter_flags = new_filter_flags

        for flag in filter_flags:
            if not hasattr(self.qc, flag):
                raise ValueError(
                    f"The attribute '{flag}' does not exist in the QC attributes of the sonde object. "
                    "Please ensure that the flag names provided in 'filter_flags' correspond to existing QC attributes. "
                    "If you're using a prefix to filter attributes, make sure the prefix is correct. "
                    "Check your skipped QC functions or your provided list of filter flags."
                )
            if not bool(getattr(self.qc, flag)):
                print(
                    f"{flag} returned False. Therefore, filtering this sonde ({self.serial_id}) out from L2"
                )
                return None

        # If the sonde passes all the QC checks, remove all attributes listed in filter_flags
        for flag in filter_flags:
            delattr(self.qc, flag)

        return self

    def create_interim_l2_ds(self):
        """
        Creates an interim L2 dataset from the aspen_ds or cropped_aspen_ds attribute.

        Parameters
        ----------
        None

        Returns
        -------
        self : object
            Returns the sonde object with the interim L2 dataset added as an attribute.
        """
        if self.is_floater:
            if not hasattr(self, "cropped_aspen_ds"):
                self.crop_aspen_ds_to_landing_time()
            ds = self.cropped_aspen_ds
        else:
            ds = self.aspen_ds

        object.__setattr__(self, "_interim_l2_ds", ds)

        return self

    def convert_to_si(self, variables=["rh", "pres", "tdry"], skip=False):
        """
        Converts variables to SI units.

        Parameters
        ----------
        variables : list or str, optional
            The variables to convert to SI units. If a string is provided, it should be a comma-separated list of variables.
            The default variables are 'rh', 'pres', and 'tdry'.

        skip : bool, optional
            If set to True, the function will skip the conversion process but will still ensure that the '_interim_l2_ds' attribute is set.
            If '_interim_l2_ds' is not already an attribute of the object, it will be set to 'aspen_ds'.
            Default is False.

        Returns
        -------
        self : object
            Returns the sonde object with the specified variables in aspen_ds converted to SI units.
            If 'skip' is set to True, it returns the sonde object with '_interim_l2_ds' set to 'aspen_ds' if it wasn't already present.
        """
        if hh.get_bool(skip):
            if hasattr(self, "_interim_l2_ds"):
                return self
            else:
                object.__setattr__(self, "_interim_l2_ds", self.aspen_ds)
                return self
        else:
            if isinstance(variables, str):
                variables = variables.split(",")

            if hasattr(self, "_interim_l2_ds"):
                ds = self._interim_l2_ds
            else:
                ds = self.aspen_ds

            for variable in variables:
                func = hh.get_si_converter_function_based_on_var(variable)
                ds = ds.assign({f"{variable}": func(self.aspen_ds[variable])})

            object.__setattr__(self, "_interim_l2_ds", ds)

            return self

    def get_l2_variables(self, l2_variables: dict = hh.l2_variables):
        """
        Gets the variables from aspen_ds to create L2.

        Parameters
        ----------
        l2_variables : dict or str, optional
            A dictionary where the keys are the variables in aspen_ds to keep for L2.
            If dictionary items contain a 'rename_to' key, the variable will be renamed to the value of 'rename_to'.
            If dictionary items contain a 'attributes' key, the variable will be assigned the attributes in the value of 'attributes'.
            The default is the l2_variables dictionary from the helper module.

        Returns
        -------
        self : object
            Returns the sonde object with only the specified variables (renamed if dictionary has 'rename_to' key and attributes added if dictionary has 'attributes' key) in _interim_l2_ds attribute.
            If '_interim_l2_ds' is not already an attribute of the object, it will first be set to 'aspen_ds' before reducing to the variables and renaming.
        """
        if isinstance(l2_variables, str):
            l2_variables = ast.literal_eval(l2_variables)

        l2_variables_list = list(l2_variables.keys())

        if hasattr(self, "_interim_l2_ds"):
            ds = self._interim_l2_ds
        else:
            ds = self.aspen_ds

        ds = ds[l2_variables_list]

        for variable, variable_dict in l2_variables.items():
            if "attributes" in variable_dict:
                ds[variable].attrs = variable_dict["attributes"]
            if "rename_to" in variable_dict:
                ds = ds.rename({variable: variable_dict["rename_to"]})

        object.__setattr__(self, "_interim_l2_ds", ds)

        return self

    def add_sonde_id_variable(self, variable_name="sonde_id"):
        """
        Adds a variable and related attributes to the sonde object with the Sonde object (self)'s serial_id attribute.

        Parameters
        ----------
        variable_name : str, optional
            The name of the variable to be added. Default is 'sonde_id'.

        Returns
        -------
        self : object
            Returns the sonde object with a variable containing serial_id. Name of the variable provided by 'variable_name'.
        """
        if hasattr(self, "_interim_l2_ds"):
            ds = self._interim_l2_ds
        else:
            ds = self.aspen_ds

        ds = ds.assign({variable_name: self.serial_id})
        ds[variable_name].attrs = {
            "descripion": "unique sonde ID",
            "long_name": "sonde identifier",
            "cf_role": "trajectory_id",
        }

        object.__setattr__(self, "_interim_l2_ds", ds)

        return self

    def get_flight_attributes(
        self, l2_flight_attributes_map: dict = hh.l2_flight_attributes_map
    ) -> None:
        """
        Gets flight attributes from the A-file and adds them to the sonde object.

        Parameters
        ----------
        l2_flight_attributes_map : dict or str, optional
            A dictionary where the keys are the flight attributes in the A-file
            and the values are the corresponding (renamed) attribute names to be used for the L2 file.
            The default is the l2_flight_attributes_map dictionary from the helper module.

        Returns
        -------
        self : object
            Returns the sonde object with the flight attributes added as attributes.
        """
        flight_attrs = {}

        with open(self.afile, "r") as f:
            lines = f.readlines()

        for attr in l2_flight_attributes_map.keys():
            for line_id, line in enumerate(lines):
                if attr in line:
                    break

            attr = l2_flight_attributes_map.get(attr, attr)

            value = lines[line_id].split("= ")[1]
            flight_attrs[attr] = float(value) if "AVAPS" not in attr else value

        object.__setattr__(self, "flight_attrs", flight_attrs)

        return self

    def get_other_global_attributes(self):
        nc_global_attrs = {
            # "title": "Level-2",
            # "doi": f"{halodrops.data_doi}",
            # "created with": f"pipeline.py doi:{halodrops.software_doi}",
            "Conventions": "CF-1.8",
            "platform_id": self.platform_id,
            # "instrument_id": "Vaisala RD-41",
            "product_id": "Level-2",
            # "AVAPS_Software_version": "Version 4.1.2",
            "ASPEN_version": (
                self.aspen_ds.AspenVersion
                if hasattr(self.aspen_ds, "AspenVersion")
                else self.aspen_ds.AvapsEditorVersion
            ),
            "ASPEN_processing_time": self.aspen_ds.ProcessingTime,
            # "JOANNE_version": joanne.__version__,
            # "launch_date": str(pd.to_datetime(self.launch_time).date()),
            "launch_time_(UTC)": (
                str(self.aspen_ds.launch_time.values)
                if hasattr(self.aspen_ds, "launch_time")
                else str(self.aspen_ds.base_time.values)
            ),
            "is_floater": self.is_floater.__str__(),
            "sonde_serial_ID": self.serial_id,
            "author": "Geet George",
            "author_email": "g.george@tudelft.nl",
            "featureType": "trajectory",
            # "reference": halodrops.reference_study,
            "creation_time": str(datetime.utcnow()) + " UTC",
        }

        for attr in dir(self):
            if attr.startswith("near_surface_count_"):
                nc_global_attrs[attr] = getattr(self, attr)
            if attr.startswith("profile_fullness_fraction_"):
                nc_global_attrs[attr] = getattr(self, attr)

        for attr in dir(self.qc):
            if not attr.startswith("__"):
                nc_global_attrs[f"qc_{attr}"] = int(getattr(self.qc, attr))

        object.__setattr__(self, "nc_global_attrs", nc_global_attrs)

        return self

    def add_global_attributes_to_interim_l2_ds(self):
        """
        Adds global attributes to _interim_l2_ds.

        Parameters
        ----------
        None

        Returns
        -------
        self : object
            Returns the sonde object with global attributes added to _interim_l2_ds.
        """
        ds = self._interim_l2_ds

        attrs_to_del = []
        for attr in ds.attrs.keys():
            attrs_to_del.append(attr)

        for attr in attrs_to_del:
            del ds.attrs[attr]

        if hasattr(self, "flight_attrs"):
            for attr, value in self.flight_attrs.items():
                ds.attrs[attr] = value
        if hasattr(self, "nc_global_attrs"):
            for attr, value in self.nc_global_attrs.items():
                ds.attrs[attr] = value

        object.__setattr__(self, "_interim_l2_ds", ds)

        return self

    def add_compression_and_encoding_properties(
        self,
        encoding_variables: dict = hh.encoding_variables,
        default_variable_compression_properties: dict = hh.variable_compression_properties,
    ):
        """
        Adds compression and encoding properties to _interim_l2_ds.

        Parameters
        ----------
        comp : dict or str, optional
            A dictionary containing the compression properties to be used for the L2 file.
            The default is the comp dictionary from the helper module.

        Returns
        -------
        self : object
            Returns the sonde object with compression and encoding properties added to _interim_l2_ds.
        """

        for var in encoding_variables:
            self._interim_l2_ds[var].encoding = encoding_variables[var]

        for var in self._interim_l2_ds.data_vars:
            if not encoding_variables.get(var):
                self._interim_l2_ds[
                    var
                ].encoding = default_variable_compression_properties

        return self

    def get_l2_filename(
        self, l2_filename: str = None, l2_filename_template: str = None
    ):
        """
        Gets the L2 filename from the template provided.

        Parameters
        ----------
        l2_filename : str, optional
            The L2 filename. The default is the l2_filename_template from the helper module.

        Returns
        -------
        self : object
            Returns the sonde object with the L2 filename added as an attribute.
        """

        if l2_filename is None:
            if l2_filename_template:
                l2_filename = l2_filename_template.format(
                    platform=self.platform_id,
                    serial_id=self.serial_id,
                    flight_id=self.flight_id,
                    launch_time=self.launch_time.astype(datetime).strftime(
                        "%Y-%m-%d_%H-%M"
                    ),
                )
            else:
                l2_filename = hh.l2_filename_template.format(
                    platform=self.platform_id,
                    serial_id=self.serial_id,
                    flight_id=self.flight_id,
                    launch_time=self.launch_time.astype(datetime).strftime(
                        "%Y-%m-%d_%H-%M"
                    ),
                )

        object.__setattr__(self, "l2_filename", l2_filename)

        return self

    def write_l2(self, l2_dir: str = None):
        """
        Writes the L2 file to the specified directory.

        Parameters
        ----------
        l2_dir : str, optional
            The directory to write the L2 file to. The default is the directory of the A-file with '0' replaced by '2'.

        Returns
        -------
        self : object
            Returns the sonde object with the L2 file written to the specified directory using the l2_filename attribute to set the name.
        """

        if l2_dir is None:
            l2_dir = self.l2_dir

        if not os.path.exists(l2_dir):
            os.makedirs(l2_dir)

        self._interim_l2_ds.to_netcdf(os.path.join(l2_dir, self.l2_filename))

        return self

    def add_l2_ds(self, l2_dir: str = None):
        """
        Adds the L2 dataset as an attribute to the sonde object.

        Parameters
        ----------
        l2_dir : str, optional
            The directory to read the L2 file from. The default is the directory of the A-file with '0' replaced by '2'.

        Returns
        -------
        self : object
            Returns the sonde object with the L2 dataset added as an attribute.
        """
        if l2_dir is None:
            l2_dir = self.l2_dir

        object.__setattr__(
            self, "l2_ds", xr.open_dataset(os.path.join(l2_dir, self.l2_filename))
        )

        return self

    def create_prep_l3(self):
        _prep_l3_ds = self.l2_ds.assign_coords(
            {"sonde_id": ("sonde_id", [self.l2_ds.sonde_id.values])}
        ).sortby("time")
        object.__setattr__(self, "_prep_l3_ds", _prep_l3_ds)
        return self

    def remove_non_mono_incr_alt(self):
        """
        This function removes the indices in the
        geopotential height ('gpsalt')
        """
        _prep_l3_ds = self._prep_l3_ds.load()
        gps_alt = _prep_l3_ds.gpsalt
        curr_alt = gps_alt.isel(time=0)
        for i in range(len(gps_alt)):
            if gps_alt[i] > curr_alt:
                gps_alt[i] = np.nan
            elif ~np.isnan(gps_alt[i]):
                curr_alt = gps_alt[i]
        _prep_l3_ds["gpsalt"] = gps_alt

        mask = ~np.isnan(gps_alt)
        object.__setattr__(
            self,
            "_prep_l3_ds",
            _prep_l3_ds.sel(time=mask),
        )
        return self

    def interpolate_alt(
        self,
        interp_start=-5,
        interp_stop=14515,
        interp_step=10,
        max_gap_fill: int = 50,
        method: str = "bin",
    ):

        interpolation_grid = np.arange(interp_start, interp_stop, interp_step)

        if not (self._prep_l3_ds["gpsalt"].diff(dim="time") < 0).any():
            warnings.warn(
                f"your altitude for sonde {self._interim_l3_ds.sonde_id.values} is not sorted."
            )
        ds = self._prep_l3_ds.swap_dims({"time": "gpsalt"}).load()

        if method == "linear_interpolate":
            interp_ds = ds.interp(gpsalt=interpolation_grid)
        elif method == "bin":

            interpolation_bins = interpolation_grid.astype("int")
            interpolation_label = np.arange(
                interp_start + interp_step / 2,
                interp_stop - interp_step / 2,
                interp_step,
            )
            interp_ds = ds.groupby_bins(
                "gpsalt",
                interpolation_bins,
                labels=interpolation_label,
            ).mean(dim="gpsalt")
            # somehow coordinates are lost and need to be added again
            for coord in ["lat", "lon", "time"]:
                interp_ds = interp_ds.assign_coords(
                    {
                        coord: (
                            "gpsalt",
                            ds[coord]
                            .groupby_bins(
                                "gpsalt", interpolation_bins, labels=interpolation_label
                            )
                            .mean("gpsalt")
                            .values,
                        )
                    }
                )
            interp_ds = (
                interp_ds.transpose()
                .interpolate_na(
                    dim="gpsalt_bins", max_gap=max_gap_fill, use_coordinate=True
                )
                .rename({"gpsalt_bins": "gpsalt", "time": "interpolated_time"})
            )

        object.__setattr__(self, "_prep_l3_ds", interp_ds)

        return self

    def prepare_l2_for_gridded(self):
        """
        Prepares l2 datasets to be concatenated to gridded.
        adds all attributes as variables to avoid conflicts when concatenating because attributes are different
        (and not lose information)

        """
        _prep_l3_ds = self._prep_l3_ds
        for attr, value in self._prep_l3_ds.attrs.items():
            _prep_l3_ds[attr] = value

        _prep_l3_ds.attrs.clear()
        object.__setattr__(self, "_prep_l3_ds", _prep_l3_ds)
        return self

    def add_q_and_theta_to_l2_ds(self):
        """
        Adds potential temperature and specific humidity to the L2 dataset.

        Parameters
        ----------
        None

        Returns
        -------
        self : object
            Returns the sonde object with potential temperature and specific humidity added to the L2 dataset.
        """
        ds = self._prep_l3_ds

        ds = hh.calc_q_from_rh(ds)
        ds = hh.calc_theta_from_T(ds)

        object.__setattr__(self, "_interim_l3_ds", ds)

        return self


@dataclass(order=True)
class Gridded:
    sondes: dict
    flight_id: str
    platform_id: str

    def concat_sondes(self):
        """
        function to concatenate all sondes using the combination of all measurement times and launch times
        """
        list_of_l2_ds = [sonde._prep_l3_ds for sonde in self.sondes.values()]
        combined = xr.combine_by_coords(list_of_l2_ds)
        self._interim_l3_ds = combined
        return self

    def get_l3_dir(self, l3_dirname: str = None):
        if l3_dirname:
            self.l3_dir = l3_dirname
        elif not self.sondes is None:
            self.l3_dir = list(self.sondes.values())[0].l3_dir
        else:
            raise ValueError("No sondes and no l3 directory given, cannot continue ")

    def get_l3_filename(
        self, l3_filename_template: str = None, l3_filename: str = None
    ):
        if l3_filename is None:
            if l3_filename_template is None:
                l3_filename = hh.l3_filename_template.format(
                    platform=self.platform_id,
                    flight_id=self.flight_id,
                )
            else:
                l3_filename = l3_filename_template.format(
                    platform=self.platform_id,
                    flight_id=self.flight_id,
                )

        self.l3_filename = l3_filename

        return self

    def write_l3(self, l3_dir: str = None):
        if l3_dir is None:
            l3_dir = self.l3_dir

        if not os.path.exists(l3_dir):
            os.makedirs(l3_dir)

        self._interim_l3_ds.to_netcdf(os.path.join(l3_dir, self.l3_filename))

        return self
