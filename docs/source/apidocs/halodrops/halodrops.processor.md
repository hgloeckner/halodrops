# {py:mod}`halodrops.processor`

```{py:module} halodrops.processor
```

```{autodoc2-docstring} halodrops.processor
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Sonde <halodrops.processor.Sonde>`
  - ```{autodoc2-docstring} halodrops.processor.Sonde
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`_no_default <halodrops.processor._no_default>`
  - ```{autodoc2-docstring} halodrops.processor._no_default
    :summary:
    ```
````

### API

````{py:data} _no_default
:canonical: halodrops.processor._no_default
:value: >
   'object(...)'

```{autodoc2-docstring} halodrops.processor._no_default
```

````

`````{py:class} Sonde
:canonical: halodrops.processor.Sonde

```{autodoc2-docstring} halodrops.processor.Sonde
```

````{py:attribute} sort_index
:canonical: halodrops.processor.Sonde.sort_index
:type: numpy.datetime64
:value: >
   'field(...)'

```{autodoc2-docstring} halodrops.processor.Sonde.sort_index
```

````

````{py:attribute} serial_id
:canonical: halodrops.processor.Sonde.serial_id
:type: str
:value: >
   None

```{autodoc2-docstring} halodrops.processor.Sonde.serial_id
```

````

````{py:attribute} _
:canonical: halodrops.processor.Sonde._
:type: dataclasses.KW_ONLY
:value: >
   None

```{autodoc2-docstring} halodrops.processor.Sonde._
```

````

````{py:attribute} launch_time
:canonical: halodrops.processor.Sonde.launch_time
:type: typing.Optional[typing.Any]
:value: >
   None

```{autodoc2-docstring} halodrops.processor.Sonde.launch_time
```

````

````{py:method} __post_init__()
:canonical: halodrops.processor.Sonde.__post_init__

```{autodoc2-docstring} halodrops.processor.Sonde.__post_init__
```

````

````{py:method} add_flight_id(flight_id: str) -> None
:canonical: halodrops.processor.Sonde.add_flight_id

```{autodoc2-docstring} halodrops.processor.Sonde.add_flight_id
```

````

````{py:method} add_platform_id(platform_id: str) -> None
:canonical: halodrops.processor.Sonde.add_platform_id

```{autodoc2-docstring} halodrops.processor.Sonde.add_platform_id
```

````

````{py:method} add_spatial_coordinates_at_launch(launch_coordinates: typing.List) -> None
:canonical: halodrops.processor.Sonde.add_spatial_coordinates_at_launch

```{autodoc2-docstring} halodrops.processor.Sonde.add_spatial_coordinates_at_launch
```

````

````{py:method} add_launch_detect(launch_detect_bool: bool) -> None
:canonical: halodrops.processor.Sonde.add_launch_detect

```{autodoc2-docstring} halodrops.processor.Sonde.add_launch_detect
```

````

````{py:method} add_afile(path_to_afile: str) -> None
:canonical: halodrops.processor.Sonde.add_afile

```{autodoc2-docstring} halodrops.processor.Sonde.add_afile
```

````

````{py:method} add_level_dir()
:canonical: halodrops.processor.Sonde.add_level_dir

```{autodoc2-docstring} halodrops.processor.Sonde.add_level_dir
```

````

````{py:method} run_aspen(path_to_postaspenfile: str = None) -> None
:canonical: halodrops.processor.Sonde.run_aspen

```{autodoc2-docstring} halodrops.processor.Sonde.run_aspen
```

````

````{py:method} add_aspen_ds() -> None
:canonical: halodrops.processor.Sonde.add_aspen_ds

```{autodoc2-docstring} halodrops.processor.Sonde.add_aspen_ds
```

````

````{py:method} filter_no_launch_detect() -> None
:canonical: halodrops.processor.Sonde.filter_no_launch_detect

```{autodoc2-docstring} halodrops.processor.Sonde.filter_no_launch_detect
```

````

````{py:method} detect_floater(gpsalt_threshold: float = 25, consecutive_time_steps: int = 3, skip: bool = False)
:canonical: halodrops.processor.Sonde.detect_floater

```{autodoc2-docstring} halodrops.processor.Sonde.detect_floater
```

````

````{py:method} crop_aspen_ds_to_landing_time()
:canonical: halodrops.processor.Sonde.crop_aspen_ds_to_landing_time

```{autodoc2-docstring} halodrops.processor.Sonde.crop_aspen_ds_to_landing_time
```

````

````{py:method} profile_fullness(variable_dict={'u_wind': 4, 'v_wind': 4, 'rh': 2, 'tdry': 2, 'pres': 2}, time_dimension='time', timestamp_frequency=4, fullness_threshold=0.75, add_fullness_fraction_attribute=True, skip=False)
:canonical: halodrops.processor.Sonde.profile_fullness

```{autodoc2-docstring} halodrops.processor.Sonde.profile_fullness
```

````

````{py:method} near_surface_coverage(variables=['u_wind', 'v_wind', 'rh', 'tdry', 'pres'], alt_bounds=[0, 1000], alt_dimension_name='alt', count_threshold=50, add_near_surface_count_attribute=True, skip=False)
:canonical: halodrops.processor.Sonde.near_surface_coverage

```{autodoc2-docstring} halodrops.processor.Sonde.near_surface_coverage
```

````

````{py:method} filter_qc_fail(filter_flags=None)
:canonical: halodrops.processor.Sonde.filter_qc_fail

```{autodoc2-docstring} halodrops.processor.Sonde.filter_qc_fail
```

````

````{py:method} create_interim_l2_ds()
:canonical: halodrops.processor.Sonde.create_interim_l2_ds

```{autodoc2-docstring} halodrops.processor.Sonde.create_interim_l2_ds
```

````

````{py:method} convert_to_si(variables=['rh', 'pres', 'tdry'], skip=False)
:canonical: halodrops.processor.Sonde.convert_to_si

```{autodoc2-docstring} halodrops.processor.Sonde.convert_to_si
```

````

````{py:method} get_l2_variables(l2_variables: dict = hh.l2_variables)
:canonical: halodrops.processor.Sonde.get_l2_variables

```{autodoc2-docstring} halodrops.processor.Sonde.get_l2_variables
```

````

````{py:method} add_sonde_id_variable(variable_name='sonde_id')
:canonical: halodrops.processor.Sonde.add_sonde_id_variable

```{autodoc2-docstring} halodrops.processor.Sonde.add_sonde_id_variable
```

````

````{py:method} get_flight_attributes(l2_flight_attributes_map: dict = hh.l2_flight_attributes_map) -> None
:canonical: halodrops.processor.Sonde.get_flight_attributes

```{autodoc2-docstring} halodrops.processor.Sonde.get_flight_attributes
```

````

````{py:method} get_other_global_attributes()
:canonical: halodrops.processor.Sonde.get_other_global_attributes

```{autodoc2-docstring} halodrops.processor.Sonde.get_other_global_attributes
```

````

````{py:method} add_global_attributes_to_interim_l2_ds()
:canonical: halodrops.processor.Sonde.add_global_attributes_to_interim_l2_ds

```{autodoc2-docstring} halodrops.processor.Sonde.add_global_attributes_to_interim_l2_ds
```

````

````{py:method} add_compression_and_encoding_properties(encoding_variables: dict = hh.encoding_variables, default_variable_compression_properties: dict = hh.variable_compression_properties)
:canonical: halodrops.processor.Sonde.add_compression_and_encoding_properties

```{autodoc2-docstring} halodrops.processor.Sonde.add_compression_and_encoding_properties
```

````

````{py:method} get_l2_filename(l2_filename: str = None, l2_filename_template: str = None)
:canonical: halodrops.processor.Sonde.get_l2_filename

```{autodoc2-docstring} halodrops.processor.Sonde.get_l2_filename
```

````

````{py:method} write_l2(l2_dir: str = None)
:canonical: halodrops.processor.Sonde.write_l2

```{autodoc2-docstring} halodrops.processor.Sonde.write_l2
```

````

````{py:method} add_l2_ds(l2_dir: str = None)
:canonical: halodrops.processor.Sonde.add_l2_ds

```{autodoc2-docstring} halodrops.processor.Sonde.add_l2_ds
```

````

````{py:method} add_q_and_theta_to_l2_ds()
:canonical: halodrops.processor.Sonde.add_q_and_theta_to_l2_ds

```{autodoc2-docstring} halodrops.processor.Sonde.add_q_and_theta_to_l2_ds
```

````

`````
