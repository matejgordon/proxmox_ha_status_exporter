#!/usr/bin/python
import requests
import sys, errno
import argparse
import yaml
from prometheus_client import start_http_server, Gauge
import time
import logging
import socket

# Set logging level
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Parse arguments from the command line
def parse_arguments():
    parser = argparse.ArgumentParser(description='Enable HA state for a VM in Proxmox')
    parser.add_argument('--config-file', type=str, default='./config/proxmox_ha_status_exporter.yml', help='Config file location')
    parser.add_argument('--port', type=int, default=9562, help='Port number for the server')
    return parser.parse_args()

# Fuction to authenticate and get token
def authenticate(proxmox_node, proxmox_user, proxmox_password, verify_ssl, proxmox_node_port):
    """Authenticate and get token."""
    auth_url = f"https://{proxmox_node}:{proxmox_node_port}/api2/json/access/ticket"
    auth_data = {
        "username": proxmox_user,
        "password": proxmox_password
    }
    def check_ip_availability(ip, port):
        """Check if the IP is available on the specified port."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Set a timeout of 2 seconds
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0

    # Check if the IP is available before making the request
    if check_ip_availability(proxmox_node, proxmox_node_port):
        try:
            response = requests.post(auth_url, data=auth_data, verify=verify_ssl)
            auth_response = response.json()
        except requests.exceptions.SSLError as e:
            logging.error(f"SSL verification failed: {e}")
            if verify_ssl:
                logging.warning("SSL verification is enabled. Please check the certificate. If it's self-signed, you can disable SSL verification by setting verify_ssl to false in the config file.")
            sys.exit(errno.EACCES)
        if str(auth_response) == "{'data': None}":
            logging.error("Authentication to the PVE unsuccessful")
            sys.exit(errno.EACCES)
        # Extract ticket and CSRFPreventionToken
        ticket = auth_response['data']['ticket']
        csrf_token = auth_response['data']['CSRFPreventionToken']
        cookies = {
            'PVEAuthCookie': ticket
        }
        headers = {
            'CSRFPreventionToken': csrf_token
        }
        logging.info(f"Authenticated to Proxmox node {proxmox_node} on port {proxmox_node_port}")
        return cookies, headers
    else:
        logging.error(f"Proxmox node {proxmox_node} is not available on port {proxmox_node_port}. Please check the IP and port.")
        sys.exit(errno.EACCES)

VM_STATE = Gauge('vm_state', 'State of the VM', ['id', 'node', 'group'])
def process_vm_state(vm_state):
    """Parse VM state and update Prometheus metrics."""
    # Remove previous state from reporting
    VM_STATE.clear()
    
    for vm in vm_state:
        if 'service' in vm['id']:
            VM_STATE.labels(id=vm['id'], node=vm['node'], group=vm.get('group', 'N/A')).set(get_state_number(vm['state']))
def get_state_number(state):
    """Map VM state to corresponding number."""
    state_mapping = {
        'stopped': 0,
        'request_stop': 1,
        'stopping': 2,
        'started': 3,
        'starting': 4,
        'fence': 5,
        'recovery': 6,
        'freeze': 7,
        'ignored': 8,
        'migrate': 9,
        'error': 10,
        'queued': 11,
        'disabled': 12
    }
    return state_mapping.get(state, -1)

def main():
    # Parse arguments adn read config file
    args = parse_arguments()
    try:
        with open(str(args.config_file)) as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        logging.error(f"Config file not found: {e}")
        sys.exit(errno.ENOENT)
    except yaml.YAMLError as e:
        logging.error(f"Error reading config file: {e}")
        sys.exit(errno.EINVAL)
    
    proxmox_node = config["default"]["proxmox_node"]
    proxmox_user = config["default"]["user"]
    proxmox_password = config["default"]["password"]
    verify_ssl = config["default"].get("verify_ssl", True)
    scrape_interval = config["default"].get("scrape_interval", 60)
    proxmox_node_port = config["default"].get("proxmox_node_port", 8006)

    if not isinstance(proxmox_node, str):
        sys.exit("proxmox_node must be a string")
    if not isinstance(proxmox_user, str):
        sys.exit("proxmox_user must be a string")
    if not isinstance(proxmox_password, str):
        sys.exit("proxmox_password must be a string")
    if not isinstance(verify_ssl, bool):
        sys.exit("verify_ssl must be a boolean")
    if not isinstance(scrape_interval, int):
        sys.exit("scrape_interval must be an integer")
    if not isinstance(verify_ssl, bool):
        sys.exit("verify_ssl must be a boolean")

    # Disable warnings for unverified HTTPS requests if SSL verification is disabled
    if verify_ssl == False:
        requests.packages.urllib3.disable_warnings()

    start_http_server(args.port)
    logging.info(f"Server started on http://0.0.0.0:{args.port}")

    cookies, headers = authenticate(proxmox_node, proxmox_user, proxmox_password, verify_ssl, proxmox_node_port)
    data_url = f"https://{proxmox_node}:{proxmox_node_port}/api2/json/cluster/ha/status/current"

    while True:
        try:
            ha_response = requests.get(data_url, cookies=cookies, headers=headers, verify=verify_ssl).json()
        except requests.exceptions.SSLError as e:
            logging.error(f"SSL verification failed: {e}")
            if verify_ssl:
                logging.warning("SSL verification is enabled. Please check the certificate. If it's self-signed, you can disable SSL verification by setting verify_ssl to false in the config file.")
            sys.exit(errno.EACCES)

        process_vm_state(ha_response["data"])
        time.sleep(scrape_interval)


if __name__ == '__main__':
    main()
