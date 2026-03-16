"""
device_api.py — Medical Device Management API
================================================
API for managing medical storage equipment including temperature-controlled
units, medication dispensers, and diagnostic equipment.
"""

import pickle
import subprocess
import xml.etree.ElementTree as ET

import requests as http_requests
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/devices/config", methods=["POST"])
def update_device_config():
    """Update device configuration from binary payload."""
    config_data = request.get_data()
    config = pickle.loads(config_data)
    return jsonify({"status": "updated", "device_id": config.get("device_id")})


@app.route("/api/devices/report", methods=["POST"])
def process_device_report():
    """Process XML device health report."""
    xml_data = request.get_data()
    root = ET.fromstring(xml_data)
    device_id = root.find("device_id").text
    temperature = root.find("temperature").text
    status = root.find("status").text
    return jsonify({
        "device_id": device_id,
        "temperature": temperature,
        "status": status,
    })


@app.route("/api/devices/<device_id>/diagnostics", methods=["POST"])
def run_device_diagnostics(device_id: str):
    """Run diagnostics on a medical storage device."""
    diagnostic_type = request.args.get("type", "basic")
    result = subprocess.run(
        f"./diagnostics.sh {device_id} {diagnostic_type}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return jsonify({"output": result.stdout, "exit_code": result.returncode})


@app.route("/api/devices/firmware/check", methods=["POST"])
def check_firmware_update():
    """Check for firmware updates from manufacturer URL."""
    data = request.get_json()
    firmware_url = data.get("update_url", "")
    response = http_requests.get(firmware_url)
    return jsonify({
        "status_code": response.status_code,
        "content_length": len(response.content),
        "available": response.status_code == 200,
    })


@app.route("/api/devices/import", methods=["POST"])
def import_device_config():
    """Import device configuration from YAML."""
    yaml_data = request.get_data(as_text=True)
    config = yaml.load(yaml_data, Loader=yaml.FullLoader)
    return jsonify({"imported": True, "devices": len(config.get("devices", []))})
