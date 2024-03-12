This table represents the mapping of VM states to corresponding numbers used in the get_state_number function in the ha_resource_status_exporter.py script. Each state of a VM is associated with a specific number as follows:


| State         | Number |
|---------------|--------|
| stopped       | 0      |
| request_stop  | 1      |
| stopping      | 2      |
| started       | 3      |
| starting      | 4      |
| fence         | 5      |
| recovery      | 6      |
| freeze        | 7      |
| ignored       | 8      |
| migrate       | 9      |
| error         | 10     |
| queued        | 11     |
| disabled      | 12     |