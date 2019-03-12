# TemperUSB Exporter
Prometheus exporter to display metrics from TemperUSB device(s).

## Requirements
* Python v3
* Following pip3 packages: `prometheus_client pyserial`

## Usage
```py
./temperusb_exporter
```
> No arguments needed.

## Supported TemperUSB Devices
| Product | Id | Firmware | Temp | Hum | Notes |
| ---- | ---- | ---- | ---- | ---- | ---- |
| TEMPer | 0c45:7401 | TEMPerF1.4 | I | | Metal |
| TEMPer | 413d:2107 | TEMPerGold_V3.1 | I | | Metal |
| TEMPerHUM | 413d:2107 | TEMPerX_V3.1 | I |	I | White plastic |
| TEMPer2 | 413d:2107 | TEMPerX_V3.3 | I,E | | White plastic |
| TEMPer1F | 413d:2107 | TEMPerX_V3.3 | E | | White plastic |
| TEMPerX232 | 1a86:5523 | TEMPerX232_V2.0 | I,E | I | White plastic |

## Example Metrics
This was tested with `TEMPerGold_V3.1`:
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 355.0
python_gc_objects_collected_total{generation="1"} 7.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 44.0
python_gc_collections_total{generation="1"} 3.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="7",version="3.6.7"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.0683136e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.1315584e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.55242933565e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.24
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP temperusb_celsius Internal/External temperature in Celsius.
# TYPE temperusb_celsius gauge
temperusb_celsius{busnum="1",devnum="21",firmware="TEMPerGold_V3.1",type="internal",vendor_id="16701"} 29.25
# HELP temperusb_humidity Internal/External humidity in % (0-100).
# TYPE temperusb_humidity gauge
```

## Credit
`temper.py` was created by urwen and this person along with the project can be found [here](https://github.com/urwen/temper).