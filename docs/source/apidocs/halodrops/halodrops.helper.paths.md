# {py:mod}`halodrops.helper.paths`

```{py:module} halodrops.helper.paths
```

```{autodoc2-docstring} halodrops.helper.paths
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Platform <halodrops.helper.paths.Platform>`
  - ```{autodoc2-docstring} halodrops.helper.paths.Platform
    :summary:
    ```
* - {py:obj}`Flight <halodrops.helper.paths.Flight>`
  - ```{autodoc2-docstring} halodrops.helper.paths.Flight
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`module_logger <halodrops.helper.paths.module_logger>`
  - ```{autodoc2-docstring} halodrops.helper.paths.module_logger
    :summary:
    ```
````

### API

````{py:data} module_logger
:canonical: halodrops.helper.paths.module_logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} halodrops.helper.paths.module_logger
```

````

`````{py:class} Platform(data_directory, platform_id, platform_directory_name=None, path_structure=path_to_flight_ids)
:canonical: halodrops.helper.paths.Platform

```{autodoc2-docstring} halodrops.helper.paths.Platform
```

```{rubric} Initialization
```

```{autodoc2-docstring} halodrops.helper.paths.Platform.__init__
```

````{py:method} get_flight_ids()
:canonical: halodrops.helper.paths.Platform.get_flight_ids

```{autodoc2-docstring} halodrops.helper.paths.Platform.get_flight_ids
```

````

`````

`````{py:class} Flight(data_directory, flight_id, platform_id, path_structure=path_to_l0_files)
:canonical: halodrops.helper.paths.Flight

```{autodoc2-docstring} halodrops.helper.paths.Flight
```

```{rubric} Initialization
```

```{autodoc2-docstring} halodrops.helper.paths.Flight.__init__
```

````{py:method} get_all_afiles()
:canonical: halodrops.helper.paths.Flight.get_all_afiles

```{autodoc2-docstring} halodrops.helper.paths.Flight.get_all_afiles
```

````

````{py:method} quicklooks_path()
:canonical: halodrops.helper.paths.Flight.quicklooks_path

```{autodoc2-docstring} halodrops.helper.paths.Flight.quicklooks_path
```

````

````{py:method} populate_sonde_instances() -> typing.Dict
:canonical: halodrops.helper.paths.Flight.populate_sonde_instances

```{autodoc2-docstring} halodrops.helper.paths.Flight.populate_sonde_instances
```

````

`````
