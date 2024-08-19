import numpy as np
import metpy.calc as mpcalc
from metpy.units import units

# Keys in l2_variables should be variable names in aspen_ds attribute of Sonde object
l2_variables = {
    "u_wind": {
        "rename_to": "u",
        "attributes": {
            "standard_name": "eastward_wind",
            "long_name": "u component of winds",
            "units": "m s-1",
            "coordinates": "time lon lat alt",
        },
    },
    "v_wind": {
        "rename_to": "v",
        "attributes": {
            "standard_name": "northward_wind",
            "long_name": "v component of winds",
            "units": "m s-1",
            "coordinates": "time lon lat alt",
        },
    },
    "tdry": {
        "rename_to": "ta",
        "attributes": {
            "standard_name": "air_temperature",
            "long_name": "air temperature",
            "units": "K",
            "coordinates": "time lon lat alt",
        },
    },
    "pres": {
        "rename_to": "p",
        "attributes": {
            "standard_name": "air_pressure",
            "long_name": "atmospheric pressure",
            "units": "Pa",
            "coordinates": "time lon lat alt",
        },
    },
    "rh": {
        "attributes": {
            "standard_name": "relative_humidity",
            "long_name": "relative humidity",
            "units": "",
            "coordinates": "time lon lat alt",
        }
    },
    "lat": {
        "attributes": {
            "standard_name": "latitude",
            "long_name": "latitude",
            "units": "degree_north",
            "axis": "Y",
        }
    },
    "lon": {
        "attributes": {
            "standard_name": "longitude",
            "long_name": "longitude",
            "units": "degree_east",
            "axis": "X",
        }
    },
    "time": {
        "attributes": {
            "standard_name": "time",
            "long_name": "time of recorded measurement",
            "axis": "T",
        }
    },
    "gpsalt": {
        "attributes": {
            "standard_name": "altitude",
            "long_name": "gps reported altitude above MSL",
            "units": "m",
            "axis": "Z",
            "positive": "up",
        }
    },
}

encoding_variables = {
    "time": {"units": "seconds since 1970-01-01", "dtype": "float"},
}

variable_compression_properties = dict(
    zlib=True,
    complevel=4,
    fletcher32=True,
    _FillValue=np.finfo("float32").max,
)


l2_flight_attributes_map = {
    "True Air Speed (m/s)": "true_air_speed_(ms-1)",
    "Ground Speed (m/s)": "ground_speed_(ms-1)",
    "Software Notes": "AVAPS_software_notes",
    "Format Notes": "AVAPS_format_notes",
    "True Heading (deg)": "true_heading_(deg)",
    "Ground Track (deg)": "ground_track_(deg)",
    "Longitude (deg)": "aircraft_longitude_(deg_E)",
    "Latitude (deg)": "aircraft_latitude_(deg_N)",
    "MSL Altitude (m)": "aircraft_msl_altitude_(m)",
    "Geopotential Altitude (m)": "aircraft_geopotential_altitude_(m)",
}


path_to_flight_ids = "{platform}/Level_0"
path_to_l0_files = "{platform}/Level_0/{flight_id}"

l2_filename_template = "{platform}_{launch_time}_{flight_id}_{serial_id}_Level_2.nc"

l3_filename_template = "{platform}_{flight_id}_Level_3.nc"


def get_bool(s):
    if isinstance(s, bool):
        return s
    elif isinstance(s, int):
        return bool(s)
    elif isinstance(s, str):
        lower_s = s.lower()
        if lower_s == "true":
            return True
        elif lower_s == "false":
            return False
        elif lower_s in ["0", "1"]:
            return bool(int(lower_s))
        else:
            raise ValueError(f"Cannot convert {s} to boolean")
    else:
        raise ValueError(f"Cannot convert {s} to boolean")


def convert_rh_to_si(value):
    """convert RH from % to fraction"""
    return value / 100


def convert_pres_to_si(value):
    """convert pressure from hPa to Pa"""
    return value * 100


def convert_tdry_to_si(value):
    """convert temperature from C to K"""
    return value + 273.15


def get_si_converter_function_based_on_var(var_name):
    """get the function to convert a variable to SI units based on its name"""
    func_name = f"convert_{var_name}_to_si"
    func = globals().get(func_name, None)
    if func is None:
        raise ValueError(f"No function named {func_name} found in the module")
    return func


def calc_saturation_pressure(temperature_K, method="hardy1998"):
    """
    Calculate saturation water vapor pressure

    Input
    -----
    temperature_K : array
        array of temperature in Kevlin or dew point temperature for actual vapor pressure
    method : str
        Formula used for calculating the saturation pressure
            'hardy1998' : ITS-90 Formulations for Vapor Pressure, Frostpoint Temperature,
                Dewpoint Temperature, and Enhancement Factors in the Range –100 to +100 C,
                Bob Hardy, Proceedings of the Third International Symposium on Humidity and Moisture,
                1998 (same as used in Aspen software after May 2018)

    Return
    ------
    e_sw : array
        saturation pressure (Pa)

    Examples
    --------
    >>> calc_saturation_pressure([273.15])
    array([ 611.2129107])

    >>> calc_saturation_pressure([273.15, 293.15, 253.15])
    array([  611.2129107 ,  2339.26239586,   125.58350529])
    """

    if method == "hardy1998":
        g = np.empty(8)
        g[0] = -2.8365744 * 10**3
        g[1] = -6.028076559 * 10**3
        g[2] = 1.954263612 * 10**1
        g[3] = -2.737830188 * 10 ** (-2)
        g[4] = 1.6261698 * 10 ** (-5)
        g[5] = 7.0229056 * 10 ** (-10)
        g[6] = -1.8680009 * 10 ** (-13)
        g[7] = 2.7150305

        e_sw = np.zeros_like(temperature_K)

        for t, temp in enumerate(temperature_K):
            ln_e_sw = np.sum([g[i] * temp ** (i - 2) for i in range(0, 7)]) + g[
                7
            ] * np.log(temp)
            e_sw[t] = np.exp(ln_e_sw)
        return e_sw


def calc_q_from_rh(ds):
    """
    Input :

        ds : Dataset

    Output :

        q : Specific humidity values

    Function to estimate specific humidity from the relative humidity, temperature and pressure in the given dataset.
    """

    vmr = mpcalc.mixing_ratio_from_relative_humidity(
        ds["p"].values * units.Pa,
        ds.ta.values * units.kelvin,
        (ds.rh * 100) * units.percent,
    )
    q = mpcalc.specific_humidity_from_mixing_ratio(vmr)

    ds["q"] = (ds.rh.dims, q.magnitude)
    ds["q"].attrs = dict(
        standard_name="specific humidity",
        long_name="specific humidity",
        units=str(q.units),
    )

    return ds


def calc_theta_from_T(ds):
    """
    Input :

        dataset : Dataset

    Output :

        theta : Potential temperature values

    Function to estimate potential temperature from the temperature and pressure in the given dataset.
    """
    theta = mpcalc.potential_temperature(
        ds.p.values * units.Pa, ds.ta.values * units.kelvin
    )
    ds["theta"] = (ds.ta.dims, theta.magnitude)
    ds["theta"].attrs = dict(
        standard_name="potential temperature",
        long_name="potential temperature",
        units=str(theta.units),
    )

    return ds
