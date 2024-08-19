# Config files

Each config file has a mandatory section that contains the data directory of the dropsonde data like
```ini
[MANDATORY]
data_directory = ./example_data
```
Technically, this is everything a valid config file needs. However, you can specify the place of your flight folders and of the actual dropsonde data in an optional section. For the example data this would be
```ini
[OPTIONAL]
path_to_flight_ids = {platform}/Level_0
path_to_l0_files = {platform}/Level_0/{flight_id}
```

Other optional function parameters can be specified with their function as a section. To specify the L2 and L3 filenames this could be
```ini
[processor.Sonde.get_l2_filename]
l2_filename_template = PERCUSION_{platform}_{launch_time}_{flight_id}_{serial_id}_Level_2.nc
[processor.Gridded.get_l3_filename]
l3_filename_template = PERCUSION_{platform}_{flight_id}_Level_3.nc

```
