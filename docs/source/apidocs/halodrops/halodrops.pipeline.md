# {py:mod}`halodrops.pipeline`

```{py:module} halodrops.pipeline
```

```{autodoc2-docstring} halodrops.pipeline
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_mandatory_args <halodrops.pipeline.get_mandatory_args>`
  - ```{autodoc2-docstring} halodrops.pipeline.get_mandatory_args
    :summary:
    ```
* - {py:obj}`get_mandatory_values_from_config <halodrops.pipeline.get_mandatory_values_from_config>`
  - ```{autodoc2-docstring} halodrops.pipeline.get_mandatory_values_from_config
    :summary:
    ```
* - {py:obj}`get_nondefaults_from_config <halodrops.pipeline.get_nondefaults_from_config>`
  - ```{autodoc2-docstring} halodrops.pipeline.get_nondefaults_from_config
    :summary:
    ```
* - {py:obj}`get_args_for_function <halodrops.pipeline.get_args_for_function>`
  - ```{autodoc2-docstring} halodrops.pipeline.get_args_for_function
    :summary:
    ```
* - {py:obj}`get_platforms <halodrops.pipeline.get_platforms>`
  - ```{autodoc2-docstring} halodrops.pipeline.get_platforms
    :summary:
    ```
* - {py:obj}`create_and_populate_flight_object <halodrops.pipeline.create_and_populate_flight_object>`
  - ```{autodoc2-docstring} halodrops.pipeline.create_and_populate_flight_object
    :summary:
    ```
* - {py:obj}`iterate_Sonde_method_over_dict_of_Sondes_objects <halodrops.pipeline.iterate_Sonde_method_over_dict_of_Sondes_objects>`
  - ```{autodoc2-docstring} halodrops.pipeline.iterate_Sonde_method_over_dict_of_Sondes_objects
    :summary:
    ```
* - {py:obj}`sondes_to_gridded <halodrops.pipeline.sondes_to_gridded>`
  - ```{autodoc2-docstring} halodrops.pipeline.sondes_to_gridded
    :summary:
    ```
* - {py:obj}`iterate_method_over_dataset <halodrops.pipeline.iterate_method_over_dataset>`
  - ```{autodoc2-docstring} halodrops.pipeline.iterate_method_over_dataset
    :summary:
    ```
* - {py:obj}`gridded_to_pattern <halodrops.pipeline.gridded_to_pattern>`
  - ```{autodoc2-docstring} halodrops.pipeline.gridded_to_pattern
    :summary:
    ```
* - {py:obj}`run_substep <halodrops.pipeline.run_substep>`
  - ```{autodoc2-docstring} halodrops.pipeline.run_substep
    :summary:
    ```
* - {py:obj}`run_pipeline <halodrops.pipeline.run_pipeline>`
  - ```{autodoc2-docstring} halodrops.pipeline.run_pipeline
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`pipeline <halodrops.pipeline.pipeline>`
  - ```{autodoc2-docstring} halodrops.pipeline.pipeline
    :summary:
    ```
````

### API

````{py:function} get_mandatory_args(function)
:canonical: halodrops.pipeline.get_mandatory_args

```{autodoc2-docstring} halodrops.pipeline.get_mandatory_args
```
````

````{py:function} get_mandatory_values_from_config(config, mandatory_args)
:canonical: halodrops.pipeline.get_mandatory_values_from_config

```{autodoc2-docstring} halodrops.pipeline.get_mandatory_values_from_config
```
````

````{py:function} get_nondefaults_from_config(config: configparser.ConfigParser, obj: callable) -> dict
:canonical: halodrops.pipeline.get_nondefaults_from_config

```{autodoc2-docstring} halodrops.pipeline.get_nondefaults_from_config
```
````

````{py:function} get_args_for_function(config, function)
:canonical: halodrops.pipeline.get_args_for_function

```{autodoc2-docstring} halodrops.pipeline.get_args_for_function
```
````

````{py:function} get_platforms(config)
:canonical: halodrops.pipeline.get_platforms

```{autodoc2-docstring} halodrops.pipeline.get_platforms
```
````

````{py:function} create_and_populate_flight_object(config: configparser.ConfigParser) -> (dict[halodrops.helper.paths.Platform], dict[halodrops.processor.Sonde])
:canonical: halodrops.pipeline.create_and_populate_flight_object

```{autodoc2-docstring} halodrops.pipeline.create_and_populate_flight_object
```
````

````{py:function} iterate_Sonde_method_over_dict_of_Sondes_objects(obj: dict, functions: list, config: configparser.ConfigParser) -> dict
:canonical: halodrops.pipeline.iterate_Sonde_method_over_dict_of_Sondes_objects

```{autodoc2-docstring} halodrops.pipeline.iterate_Sonde_method_over_dict_of_Sondes_objects
```
````

````{py:function} sondes_to_gridded(sondes: dict) -> xarray.Dataset
:canonical: halodrops.pipeline.sondes_to_gridded

```{autodoc2-docstring} halodrops.pipeline.sondes_to_gridded
```
````

````{py:function} iterate_method_over_dataset(dataset: xarray.Dataset, functions: list) -> xarray.Dataset
:canonical: halodrops.pipeline.iterate_method_over_dataset

```{autodoc2-docstring} halodrops.pipeline.iterate_method_over_dataset
```
````

````{py:function} gridded_to_pattern(gridded: xarray.Dataset, config: configparser.ConfigParser) -> xarray.Dataset
:canonical: halodrops.pipeline.gridded_to_pattern

```{autodoc2-docstring} halodrops.pipeline.gridded_to_pattern
```
````

````{py:function} run_substep(previous_substep_output, substep: dict, config: configparser.ConfigParser)
:canonical: halodrops.pipeline.run_substep

```{autodoc2-docstring} halodrops.pipeline.run_substep
```
````

````{py:function} run_pipeline(pipeline: dict, config: configparser.ConfigParser)
:canonical: halodrops.pipeline.run_pipeline

```{autodoc2-docstring} halodrops.pipeline.run_pipeline
```
````

````{py:data} pipeline
:canonical: halodrops.pipeline.pipeline
:value: >
   None

```{autodoc2-docstring} halodrops.pipeline.pipeline
```

````
