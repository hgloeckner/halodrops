# Data

This data section of the handbook outlines procedures for how to go about doing the quality control, the processing and the generation of data products.

## Data Directory Structure

Usually dropsonde data has a `platform` from which it was meassured and a `flight_id` from the exact flight it was taken from. After the processing each flight will have data on different levels of processing. `halodrops` uses the following levels.

| Level     | Description                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------- |
| `Level_0` | Contains all raw files from a flight                                                           |
| `Level_1` | Files generated from the ASPEN-processing of the D-files in Level-0                            |
| `Level_2` | Sounding files that passed additional QC tests, and exclude all soundings with no usable data  |
| `Level_3` | All sounding files in Level-2 gridded on a uniform, vertical grid, with some derived variables |
| `Level_4` | Circle products from all circles flown during flight                                           |


You can define your exact folder structure as shown in {doc}`example configs <../tutorial/configs>`
