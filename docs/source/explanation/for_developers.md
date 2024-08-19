# For Developers

## How does `halodrops.__init__` work?

The idea is to minimize the decision-making on the user's part. The user should be able to run the package with minimal configuration. The package should be able to handle the rest. For this, all functions in the package should ideally have all arguments with default values. The user can override these default values by providing non-default values in a configuration file.

However, some arguments cannot have default values (e.g. `data_directory` or `flight_id`). These arguments are mandatory and must be provided by the user within a `MANDATORY` section in the configuration file. This means that functions in the package that have the same mandatory arguments must always use the same argument name across the whole package (e.g. `data_directory` should not be called by a different function as `data_dir`).

The package handles these non-default and mandatory values and executes the functions with the provided arguments.

This `__init__` script thus retrieves mandatory and non-default values from the configuration file for functions within the package and its subpackages, and executes those functions with the retrieved arguments.

### Functions
`__init__` defines several functions:

`get_all_defaults(package)`: This function retrieves the default values of all functions within a package and its subpackages. It returns a dictionary where the keys are the fully qualified names of the functions, and the values are dictionaries containing the default values of the function parameters.

`nondefault_values_from_config(config, default_dict)`: This function retrieves non-default argument values from a configuration file. It returns a dictionary containing the non-default arguments and their corresponding values based on the config file.

`get_mandatory_args(function)`: This function retrieves a list of all arguments that do not have a default value for a given function.

`get_mandatory_values_from_config(config, mandatory_args)`: This function extracts mandatory values from the 'MANDATORY' section of a configuration file. It returns a dictionary where the keys are the argument names and the values are the corresponding values from the config file.

### Main Execution
The script's main execution begins by parsing command-line arguments to get the path to a configuration file. It then checks if the provided directory and file exist. If they do, it reads the configuration file.

Next, it retrieves the default values for all functions within the halodrops package using the `get_all_defaults` function. It then retrieves the non-default values from the configuration file using the `nondefault_values_from_config` function.

The script then defines a list of functions to execute. For each function, it retrieves the non-default arguments from the previously retrieved non-default values. If the function has mandatory arguments, it retrieves their values from the configuration file using the `get_mandatory_values_from_config` function.

Finally, the script executes each function with the retrieved arguments.
