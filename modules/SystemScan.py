#!/usr/bin/env python3
"""
SystemScan.py
Author: William Walker
Purpose: Collect basic system metadata from a compromised Linux host.

This module can be:
1. Run standalone (prints results to terminal)
2. Imported by fullInfoScan.py (returns results as a dict)
"""

import platform
import socket
import subprocess
import json
import os


def get_host():
    try:
        return socket.gethost()
    except Exception:
        return None


def get_os():
    try:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    except Exception:
        return None


def get_kernel():
    try:
        result = subprocess.check_output(["uname", "-r"], text=True).strip()
        return result
    except Exception:
        return None


def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.read().split()[0])
            return uptime_seconds
    except Exception:
        return None


def get_users():
    try:
        with open("/etc/passwd", "r") as f:
            users = [line.split(":")[0] for line in f.readlines()]
            return users
    except Exception:
        return None


def get_interfaces():
    try:
        result = subprocess.check_output(["ip", "-o", "addr"], text=True)
        return result.splitlines()
    except Exception:
        return None

"""
Main function used by fullInfoScan.py
Returns a dictionary of collected system information.
"""
def run():

    data = {
        "host": get_host(),
        "os": get_os(),
        "kernel": get_kernel(),
        "uptime_seconds": get_uptime(),
        "users": get_users(),
        "interfaces": get_interfaces()
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