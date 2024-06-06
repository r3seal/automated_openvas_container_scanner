import subprocess
from getIP import *
import ipaddress


def run_command(command):
    """Run a system command and return the output."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


if __name__ == "__main__":
    # Perform network scanning and write results to hostIPS.txt
    host_ip, host_mask = get_host_ip_and_mask()
    if host_ip and host_mask:
        network = ipaddress.IPv4Network(f"{host_ip}/{host_mask}", strict=False)
        active_hosts = scan_network(network)
        active_hosts.remove(host_ip)
        try:
            active_hosts.remove(get_default_gateway())
        except:
            pass
        with open("../scripts_data/hostIPS.txt", "w") as f:
            for IP in active_hosts:
                f.write(f"{IP}\n")
                
