# {py:mod}`halodrops.helper`

```{py:module} halodrops.helper
```

```{autodoc2-docstring} halodrops.helper
:allowtitles:
```

## Submodules

```{toctree}
:titlesonly:
:maxdepth: 1

halodrops.helper.rawreader
halodrops.helper.paths
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_bool <halodrops.helper.get_bool>`
  - ```{autodoc2-docstring} halodrops.helper.get_bool
    :summary:
    ```
* - {py:obj}`convert_rh_to_si <halodrops.helper.convert_rh_to_si>`
  - ```{autodoc2-docstring} halodrops.helper.convert_rh_to_si
    :summary:
    ```
* - {py:obj}`convert_pres_to_si <halodrops.helper.convert_pres_to_si>`
  - ```{autodoc2-docstring} halodrops.helper.convert_pres_to_si
    :summary:
    ```
* - {py:obj}`convert_tdry_to_si <halodrops.helper.convert_tdry_to_si>`
  - ```{autodoc2-docstring} halodrops.helper.convert_tdry_to_si
    :summary:
    ```
* - {py:obj}`get_si_converter_function_based_on_var <halodrops.helper.get_si_converter_function_based_on_var>`
  - ```{autodoc2-docstring} halodrops.helper.get_si_converter_function_based_on_var
    :summary:
    ```
* - {py:obj}`calc_saturation_pressure <halodrops.helper.calc_saturation_pressure>`
  - ```{autodoc2-docstring} halodrops.helper.calc_saturation_pressure
    :summary:
    ```
* - {py:obj}`calc_q_from_rh <halodrops.helper.calc_q_from_rh>`
  - ```{autodoc2-docstring} halodrops.helper.calc_q_from_rh
    :summary:
    ```
* - {py:obj}`calc_theta_from_T <halodrops.helper.calc_theta_from_T>`
  - ```{autodoc2-docstring} halodrops.helper.calc_theta_from_T
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`l2_variables <halodrops.helper.l2_variables>`
  - ```{autodoc2-docstring} halodrops.helper.l2_variables
    :summary:
    ```
* - {py:obj}`encoding_variables <halodrops.helper.encoding_variables>`
  - ```{autodoc2-docstring} halodrops.helper.encoding_variables
    :summary:
    ```
* - {py:obj}`variable_compression_properties <halodrops.helper.variable_compression_properties>`
  - ```{autodoc2-docstring} halodrops.helper.variable_compression_properties
    :summary:
    ```
* - {py:obj}`path_to_flight_ids <halodrops.helper.path_to_flight_ids>`
  - ```{autodoc2-docstring} halodrops.helper.path_to_flight_ids
    :summary:
    ```
* - {py:obj}`path_to_l0_files <halodrops.helper.path_to_l0_files>`
  - ```{autodoc2-docstring} halodrops.helper.path_to_l0_files
    :summary:
    ```
* - {py:obj}`l2_flight_attributes_map <halodrops.helper.l2_flight_attributes_map>`
  - ```{autodoc2-docstring} halodrops.helper.l2_flight_attributes_map
    :summary:
    ```
* - {py:obj}`l2_filename_template <halodrops.helper.l2_filename_template>`
  - ```{autodoc2-docstring} halodrops.helper.l2_filename_template
    :summary:
    ```
````

### API

````{py:data} l2_variables
:canonical: halodrops.helper.l2_variables
:value: >
   None

```{autodoc2-docstring} halodrops.helper.l2_variables
```

````

````{py:data} encoding_variables
:canonical: halodrops.helper.encoding_variables
:value: >
   None

```{autodoc2-docstring} halodrops.helper.encoding_variables
```

````

````{py:data} variable_compression_properties
:canonical: halodrops.helper.variable_compression_properties
:value: >
   'dict(...)'

```{autodoc2-docstring} halodrops.helper.variable_compression_properties
```

````

````{py:data} path_to_flight_ids
:canonical: halodrops.helper.path_to_flight_ids
:value: >
   '{platform}/Level_0'

```{autodoc2-docstring} halodrops.helper.path_to_flight_ids
```

````

````{py:data} path_to_l0_files
:canonical: halodrops.helper.path_to_l0_files
:value: >
   '{platform}/Level_0/{flight_id}'

```{autodoc2-docstring} halodrops.helper.path_to_l0_files
```

````

````{py:data} l2_flight_attributes_map
:canonical: halodrops.helper.l2_flight_attributes_map
:value: >
   None

```{autodoc2-docstring} halodrops.helper.l2_flight_attributes_map
```

````

````{py:data} l2_filename_template
:canonical: halodrops.helper.l2_filename_template
:value: >
   '{platform}_{launch_time}_{flight_id}_{serial_id}_Level_2.nc'

```{autodoc2-docstring} halodrops.helper.l2_filename_template
```

````

````{py:function} get_bool(s)
:canonical: halodrops.helper.get_bool

```{autodoc2-docstring} halodrops.helper.get_bool
```
````

````{py:function} convert_rh_to_si(value)
:canonical: halodrops.helper.convert_rh_to_si

```{autodoc2-docstring} halodrops.helper.convert_rh_to_si
```
````

````{py:function} convert_pres_to_si(value)
:canonical: halodrops.helper.convert_pres_to_si

```{autodoc2-docstring} halodrops.helper.convert_pres_to_si
```
````

````{py:function} convert_tdry_to_si(value)
:canonical: halodrops.helper.convert_tdry_to_si

```{autodoc2-docstring} halodrops.helper.convert_tdry_to_si
```
````

````{py:function} get_si_converter_function_based_on_var(var_name)
:canonical: halodrops.helper.get_si_converter_function_based_on_var

```{autodoc2-docstring} halodrops.helper.get_si_converter_function_based_on_var
```
````

````{py:function} calc_saturation_pressure(temperature_K, method='hardy1998')
:canonical: halodrops.helper.calc_saturation_pressure

```{autodoc2-docstring} halodrops.helper.calc_saturation_pressure
```
````

````{py:function} calc_q_from_rh(ds)
:canonical: halodrops.helper.calc_q_from_rh

```{autodoc2-docstring} halodrops.helper.calc_q_from_rh
```
````

````{py:function} calc_theta_from_T(dataset)
:canonical: halodrops.helper.calc_theta_from_T

```{autodoc2-docstring} halodrops.helper.calc_theta_from_T
```
````
