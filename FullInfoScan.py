#!/usr/bin/env python3
"""
FullInfoScan.py
Author: William Walker
Purpose: Run all scanning modules and aggregate results into a single JSON report.

This script:
1. Calls each scan module's run() function
2. Puts all results into a dictionary
3. Saves the final JSON to an output file 
4. Prints results ONLY if config.json says always_print = true

"""

import json
import os
import datetime
import sys

from modules import SystemScan
from modules import SSHScan
from modules import ReconScan
from modules import ProcessScan
from modules import LogScan
from modules import EnvironScan
from modules import ConfigScan
from modules import BashScan


def load_config():
    try:

        with open("config.json", "r") as f:
            return json.load(f)
        
    except Exception as e:
        print(f"ERROR: Could not load config.json, Will use DEFUALTS: {e}")
        return {"output_filename": "full_scan_output","output_number": 1,"always_print": False}


def save_config(cfg):
    try:

        with open("config.json", "w") as f:
            json.dump(cfg, f, indent=4)

    except Exception as e:
        print(f"ERROR: Could not update config.json: {e}")


def run_all_scans():
    results = {}

    try:
        results["system_info"] = SystemScan.run()
    except Exception as e:
        results["system_info"] = {"error": str(e)}

    try:
        results["ssh_keys"] = SSHScan.run()
    except Exception as e:
        results["ssh_keys"] = {"error": str(e)}

    try:
        results["recon"] = ReconScan.run()
    except Exception as e:
        results["recon"] = {"error": str(e)}

    try:
        results["process_environment"] = ProcessScan.run()
    except Exception as e:
        results["process_environment"] = {"error": str(e)}

    try:
        results["log_scan"] = LogScan.run()
    except Exception as e:
        results["log_scan"] = {"error": str(e)}

    try:
        results["environment_variables"] = EnvironScan.run()
    except Exception as e:
        results["environment_variables"] = {"error": str(e)}

    try:
        results["config_files"] = ConfigScan.run()
    except Exception as e:
        results["config_files"] = {"error": str(e)}

    try:
        results["bash_history"] = BashScan.run()
    except Exception as e:
        results["bash_history"] = {"error": str(e)}

    return results


"""
Saves the aggregated scan results to a JSON file.
"""
def save_json(data, output_path):
    try:

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
            
        return True
    
    except Exception as e:
        print(f" ERROR SAVING JSON: {e}")
        return False


"""
Main function.
Runs all scans
Saves JSON
Prints to terminal if config.json says always_print = true
"""
def main():

    cfg = load_config()

    print("Running information scan...")

    results = run_all_scans()

    now_utc = datetime.datetime.utcnow()

    results["_metadata"] = {"generated_at": now_utc.isoformat() + "Z", "generated_readable": now_utc.strftime("%B %d, %Y %H:%M UTC")}


    file_name = cfg.get("output_filename", "full_scan_output")
    num = cfg.get("output_number", 1)

    output_file = f"{file_name}_{num}.json"

    if save_json(results, output_file):
        print(f"[+] Scan results saved to {output_file}")


    cfg["output_number"] = num + 1
    save_config(cfg)

    if cfg.get("always_print", False):
        print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()