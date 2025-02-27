# C-Trace.de

Support for schedules provided by [c-trace.de](https://www.c-trace.de) which is servicing multiple municipalities.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: c_trace_de
      args:
        service: SERVICE
        ort: ORT
        strasse: STRASSE
        hausnummer: HAUSNUMMER
```

### Configuration Variables

**service**  
*(string) (required)*  
Name of the service which is specific to your municipality. See the table below to get the right value for your location.

**ort**  
*(string) (required)*

**strasse**  
*(string) (required)*

**hausnummer**  
*(string) (required)*

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: c_trace_de
      args:
        service: bremenabfallkalender
        ort: Bremen
        strasse: Abbentorstraße
        hausnummer: 5
```

## How to get the source arguments

This source requires the name of a `service` which is specific to your municipality. Use the following map to get the right value for your district.

|Municipality|service|
|-|-|
|Bremen|`bremenabfallkalender`|
|AWB Landkreis Augsburg|`augsburglandkreis`|