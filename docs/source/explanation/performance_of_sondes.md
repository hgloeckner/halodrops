
# Performance of sondes

The performance of sondes is determined by how well the sonde performs with data provision. Taking into account the "fullness" of data provided by the sonde and the data's "quality", the sondes can be categorized as either `GOOD`, `BAD` or `UGLY`. A more detailed explanation of these terms will show up here soon, as the package develops, but for now, the basis of such a classification of sondes is explained in the publication for the [JOANNE dataset](https://doi.org/10.5194/essd-13-5253-2021). The classification takes into account potential failures that a sonde might have and therefore, it is a good idea to learn about these failures.

----
## Sonde failures

Sonde failures could be because of multiple reasons:

- {ref}`Launch-detect failure <launch-detect-failure>`
- {ref}`Sensor failure <sensor-failure>`
- {ref}`Parachute failure <parachute-failure>`
- {ref}`Others <other-failure>`

(launch-detect-failure)=
### Launch-detect failure

A launch should be detected automatically in the ideal scenario. If the sonde fails to do this, it does not switch to high-power signal transmission, and thus, stops sending data back to the AVAPS PC, after a short range. The most common way this occurs is when the parachute fails to release from the sonde. There is a small IR (?) sensor in the sonde which detects that the parachute is out, and then switches on high-power radio transmission. Before this, the sonde (after initialization) transmits data to the AVAPS system via low-power transmission. Without the high-power transmission, the signal strength is too low for the aircraft to be able to detect and eventually, as the sonde goes further away, contact is lost. During EUREC4A, this was unfortunately a common failure for the HALO dropsondes, which were from a bad bunch.

The primary method to check if a launch was detected for a given sonde is to parse through the log files of the sonde. These files have names starting with 'A' (hence, called A-files) and are followed by the date and time of launch. The file extension is the number of the channel used to initialise the sonde and receive its signal, but for all practical purposes, it is a `.txt` file. (Note: For sondes that did not detect a launch, the file name has time when the sonde was initialised). The log file contains an internal record termed 'Launch Obs Done?'. If this value is 1, the launch was detected, else if it is 0, launch was not detected. The same values are used to mark the `ld_FLAG`.

To get an idea of how to get sondes that have a launch-detect failure, check out this {doc}`how-to guide <../howto/list_failed_sondes>`

(sensor-failure)=
### Sensor failure

For different reasons, any combination of the `p`, `T`, `RH`, `GPS` sensors could fail to provide measurements for the sonde. A complete failure of a sensor is easy to detect, as there would be no data at all. However, sometimes a sensor may also fail mid-trajectory and thus only provide data for a partial profile. This can be detected by looking at the `profile_coverage` of a sonde, wherein a value of 0 means no data for the entire profile and a value of 1 means data throughout the profile. A profile, in this case, is defined as the sequence of timestamps wherein potential data can be available. This can vary between sensors even for the same sonde, as the sensors have different measurement frequencies. A failure can be detected by a user-defined threshold for `profile_coverage`, e.g. profiles with `profile_coverage` < 0.4 can be one way of detecting sensor failures.

Another way that sensors might fail is by providing faulty data. This is trickier to detect. ASPEN already does some corrections in this regard, and very obvious failures should be detected. However, it is also advisable to do another sanity-check test to ensure that the sensors are providing reasonable values. For example, this could be performed by providing expected ranges for near-surface values. Sensors providing widely varying values could be considered as failures too.

(parachute-failure)=
### Parachute failure

A parachute failure is exactly what it sounds like. :) For whatever reason, the parachute does not work and the dropsonde falls at much greater descent speeds than it was designed for. In such cases, it will be detected as a "fast fall" and most likely, no measurements can be retrieved. Sometimes, this might also be due to the operator's error, wherein they forgot to remove the orange tape that restricts the parachute from releasing. A parachute failure could also lead to the launch-detect failure in cases of the RD-41 sonde.

(other-failure)=
### Others

Other ways that a sonde could fail include problems with initialization. This could be because of issues any of the steps during the initialization process.
