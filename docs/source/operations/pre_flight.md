# Pre-flight Operations

There are primarily three pre-flight operations that need to be carried out. Here, "pre-flight" has slightly different time-scales for the processes. The steps to carry out all three of the procedures are elaborated in linked PDF documents. Please note that these are from restricted documents shared with us courtesy of NCAR/EOL. Therefore, this document also should be used with that consideration in mind.

## Reconditioning of the dropsondes
```{note}
Steps for reconditioning dropsondes can be found in an [NCAR-provided document here](../resources/Reconditioning_manual.pdf)
```
A reconditioning of the dropsonde moisture sensor should be carried out within the 24 hours prior to flight operations to rid the sensor of trace-gas pollutants. Read more about the explanation for the procedure and corresponding attempts to post-correct in the [Reconditioning and Dry Bias section](../explanation/reconditioning.md).

## Sync system time with GPS time

```{note}
Steps for syncing with GPS time can be found in an [NCAR-provided document here](../resources/Sync_with_GPS_time_manual.pdf)
```

The external GPS receiver on the AVAPS rack provides a reference time for the system to be in sync with UTC. This is essential for interruption-free data collection. Please check the sync once before take-off and once before starting operations during flight.

## Test chassis cards
```{note}
Steps for testing all chassis cards can be found in an [NCAR-provided document here](../resources/System_test_manual.pdf)
```

A complete test of all of the system's chassis cards should be performed to not have any surprises during flight about components not working. Individual channel cards can be temporarily disabled, if found not to be working. However, if the sonde-interface card or GPS receiver card doesn't pass the test, these cards will have to replaced or repaired, before continuing further.
