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
        with open("inside_scripts/hostIPS.txt", "w") as f:
            for IP in active_hosts:
                f.write(f"{IP}\n")

    # # Now run Docker commands
    # commands = [
    #     'docker run --detach --publish 8080:9392 -e PASSWORD="admin" --name openvas immauss/openvas --publish 9390:9390 -e HTTPS=true',
    #     'timeout /t 10 /nobreak',
    #     'docker cp inside_scripts openvas:/',
    #     'docker exec -d -w /inside_scripts openvas python3 other_main.py'
    # ]
    #
    # for command in commands:
    #     print(f"Running command: {command}")
    #     retcode, stdout, stderr = run_command(command)
    #     if retcode != 0:
    #         print(f"Command failed with error code {retcode}. Output:\n{stderr.decode()}")
    #         exit(retcode)
    #     else:
    #         print(stdout.decode())
