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

1. Clone the repository: `git clone https://github.com/matejgordon/proxmox_ha_status_exporter.git`
2. Build the Docker image: `docker build . -t proxmox_ha_status_exporter`
3. Edit the config at `./config/proxmox_ha_status_exporter.yml`
4. Run the Docker container: `docker run -d -p 9562:9562 proxmox_ha_status_exporter` or run the sample [docker-compose](docker-compose.yml) with `docker compose up -d`
5. Access the exported data through the API endpoint.
6. Profit 💸


## Default values

### Command line configs

| directive         | required | default value |
|---------------|--------|--------|
| `--config-file`       | `no`      | `./config/proxmox_ha_status_exporter.yml`       |
| `--port`  | `no`      | `9562`      |

### Configuration file configs
The sample config file can be found [here](/config/proxmox_ha_status_exporter.yml)

| config         | required | default value |
|---------------|--------|--------|
| `proxmox_node`       | **`yes`**      | `none`      |
| `user`  | **`yes`**      | `none`      |
| `password`  | **`yes`**      | `none`      |
| `proxmox_node_port`  | `no`      | `8006`      |
| `log_level`       | `no`      | `info`      |
| `verify_ssl`      | `no`      | `true`      |
| `scrape_interval`       | `no`      | `60`      |


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


# TODO
TODO is in issue [#1](https://github.com/matejgordon/proxmox_ha_status_exporter/issues/1)