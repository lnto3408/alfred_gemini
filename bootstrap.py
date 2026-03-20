#!/usr/bin/env python3
"""Bootstrap: ensure dependencies are installed in a local venv.

Every script imports this module first. On first run it creates a venv
inside $alfred_workflow_data and pip-installs requirements.txt.
Subsequent runs just prepend the venv site-packages to sys.path.
"""

import os
import subprocess
import sys


def get_data_dir():
    d = os.environ.get("alfred_workflow_data", "")
    if not d:
        d = os.path.join(os.path.expanduser("~"), ".alfred_gemini_workflow")
    return d


def get_venv_dir():
    return os.path.join(get_data_dir(), "venv")


def get_site_packages(venv_dir):
    """Find the site-packages directory inside the venv."""
    lib_dir = os.path.join(venv_dir, "lib")
    if not os.path.isdir(lib_dir):
        return None
    for name in os.listdir(lib_dir):
        if name.startswith("python"):
            sp = os.path.join(lib_dir, name, "site-packages")
            if os.path.isdir(sp):
                return sp
    return None


def _marker_path(venv_dir):
    return os.path.join(venv_dir, ".installed")


def needs_install(venv_dir):
    """Check if we need to create/install the venv."""
    marker = _marker_path(venv_dir)
    if not os.path.exists(marker):
        return True
    # Check if requirements.txt is newer than marker
    req = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req):
        return os.path.getmtime(req) > os.path.getmtime(marker)
    return False


def install(venv_dir):
    """Create venv and install requirements."""
    python = sys.executable or "python3"
    req = os.path.join(os.path.dirname(__file__), "requirements.txt")

    # Create venv if it doesn't exist
    if not os.path.isdir(venv_dir):
        os.makedirs(os.path.dirname(venv_dir), exist_ok=True)
        subprocess.check_call(
            [python, "-m", "venv", venv_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

    # Install requirements
    pip = os.path.join(venv_dir, "bin", "pip")
    subprocess.check_call(
        [pip, "install", "-q", "-r", req],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    # Write marker
    with open(_marker_path(venv_dir), "w") as f:
        f.write("ok")


def ensure_deps():
    """Main entry point: ensure deps are available and on sys.path."""
    venv_dir = get_venv_dir()

    if needs_install(venv_dir):
        try:
            install(venv_dir)
        except subprocess.CalledProcessError as e:
            print(
                f'{{"items":[{{"title":"Dependency installation failed",'
                f'"subtitle":"Check Python 3 is available. Error: {e}",'
                f'"valid":false}}]}}',
            )
            sys.exit(1)

    sp = get_site_packages(venv_dir)
    if sp and sp not in sys.path:
        sys.path.insert(0, sp)


# Auto-run on import
ensure_deps()
