# Proxmox HA status exporter

## Description

This project is a Prometheus Proxmox HA Status Exporter that provides a mapping of VM every state to corresponding number.


# Deploy

You can run this exporter as a standalone Python script or as a Docker container.

## Standalone
### Installation

1. Clone the repository: `git clone https://github.com/matejgordon/proxmox_ha_status_exporter.git`
2. Install the required dependencies: `pip install -r requirements.txt`

### Usage

1. Edit the config at `./config/proxmox_ha_status_exporter.yml`
2. Run the `ha_resource_status_exporter.py` script.
3. Access the exported data through the API endpoint.
4. Profit 💸

## Docker
### Usage

1. Build the Docker image: `docker build -t proxmox_ha_status_exporter .`
2. Edit the config at `./config/proxmox_ha_status_exporter.yml`
3. Run the Docker container: `docker run -d -p 9562:9562 proxmox_ha_status_exporter` or use the sample [docker-compose](/config/proxmox_ha_status_exporter.yml)
4. Access the exported data through the API endpoint.
5. Profit 💸


## Default values

### Config
By default, the configuration file for the Proxmox HA Status Exporter is located at `./config/proxmox_ha_status_exporter.yml`. You can change the location with flag `--config-file`

The sample config file can be found [here](/config/proxmox_ha_status_exporter.yml)

### Port

The default port for the webserver is `9562`, but you can change it using the `--port` flag. If you are using Docker, you can map it to a different port.


# Mapping of VM States

This table represents the mapping of VM states to corresponding numbers used in the `get_state_number` function in the `ha_resource_status_exporter.py` script. Each state of a VM is associated with a specific number as follows:

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