import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor
import netifaces as ni
import subprocess


def get_host_ip_and_mask():
    try:
        # Get the hostname
        hostname = socket.gethostname()

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)

        # Get the default network interface
        default_interface = ni.gateways()['default'][ni.AF_INET][1]

        # Get the network information for the default interface
        if_info = ni.ifaddresses(default_interface)[ni.AF_INET][0]

        # Extract the netmask and calculate the network prefix length
        netmask = if_info['netmask']
        prefix_length = sum(bin(int(x)).count('1') for x in netmask.split('.'))

        return ip_address, netmask
    except Exception as e:
        return None, None


def is_host_up(ip):
    """Check if a host is reachable using the ping command."""
    try:
        # Convert the IP address to a string
        ip_str = str(ip)

        # Run the ping command to check if the host is reachable
        result = subprocess.run(['ping', '-n', '4', ip_str], capture_output=True, text=True, timeout=10)

        # Check if the command was successful (return code 0)
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False


def scan_network(network):
    net = ipaddress.ip_network(network, strict=False)
    active_hosts = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(is_host_up, net.hosts()))

    for ip, is_up in zip(net.hosts(), results):
        if is_up:
            active_hosts.append(str(ip))

    return active_hosts


def get_default_gateway():
    try:
        # Get the default gateway information
        gateway_info = ni.gateways()['default']

        # Extract the default gateway for IPv4
        default_gateway = gateway_info[ni.AF_INET][0]

        return default_gateway
    except Exception as e:
        return None
