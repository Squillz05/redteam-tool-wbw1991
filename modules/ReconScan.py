#!/usr/bin/env python3
"""
ReconScan.py
Author: William Walker
Purpose: simple recon of a compromised linux box

This module collects: Running services, Open ports, Installed packages

Can be run by itself or imported by FullInfoScan.py
"""

import subprocess
import json


def get_running_services():
    try:

        result = subprocess.check_output(["systemctl", "list-units", "--type=service", "--no-pager", "--no-legend"],text=True)

        services = []
        for line in result.splitlines():
            parts = line.split()

            if len(parts) >= 1:

                services.append(parts[0])

        return services
    

    except Exception:
        return None


def get_open_ports():
    try:

        result = subprocess.check_output(["ss", "-tuln"],text=True)
        return result.splitlines()
    
    except Exception:
        return None


def get_installed_packages():
    try:

        result = subprocess.check_output(["dpkg", "-l"],text=True)
        return result.splitlines()
    
    except Exception:
        return None


"""
Main function used by FullInfoScan.py
Returns a dict of recon info
"""
def run():

    data = {
        "running_services": get_running_services(),
        "open_ports": get_open_ports(),
        "installed_packages": get_installed_packages()
    }

    return data


"""
prints results to terminal.
"""
def alone():
    data = run()
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    alone()