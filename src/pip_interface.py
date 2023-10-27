import contextlib
import io
from collections.abc import Mapping
import sys
import os
from typing import Optional

import pip
import subprocess
import inspect
import json
import ctypes
from pip_parser import parse_pip_show

def _call_pip(command: str, *args) -> str:
    # Creates empty IO object, then writes output of pip command to that object
    # to be returned to user
    output = subprocess.run([sys.executable, "-m", "pip", command, *args], capture_output=True, text=True)
    return output.stdout


def install(package: str, constraints: list[str] = (), no_dependencies=True) -> None:
    if isinstance(constraints, str):
        constraints = [constraints]
    args = ["--no-input", package + ",".join(constraints)]
    if no_dependencies:
        args = args.append("--no_dependencies")
    _call_pip("install", "--no-input", package + ",".join(constraints))


def uninstall(package:str, reference_names: Optional[list[str]] = None) -> None:
    if reference_names is None:
        reference_names = (package,)
    # else:
    #     reference_names.append(package)
    # removes module from the cache to prevent re-installing same version
    with contextlib.suppress(KeyError):
        # del sys.modules[package]
        sys.modules.pop(package)
    # Get the frames of the Python stack, deleting all references to target package
    frames = inspect.getouterframes(frame=inspect.currentframe())
    # "frames" is a copy of the real frames
    # Update it to match what we want (no references to library)
    for frameinfo in frames:
        frame = frameinfo.frame
        for reference in reference_names:
            if reference in frame.f_locals:
                frame.f_locals.pop(reference)
            if reference in frame.f_globals:
                frame.f_globals.pop(reference)
        # Update the REAL frames to match mapping we
        # describe above
        ctypes.pythonapi.PyFrame_LocalsToFast(
            ctypes.py_object(frame),
            ctypes.c_int(1)
        )

    _call_pip("uninstall", "--no-input", "-y", package)


#TODO check what happens when package doesn't exist
def get_info(package: str) -> Mapping[str,str]:
    output = _call_pip("show", package)
    package_info = parse_pip_show(output)
    if package_info == {}:
        raise ModuleNotFoundError
    return package_info


def get_version(package: str) -> str:
    return get_info(package)["Version"]


def get_all_packages() -> Mapping[str,str]:
    result =_call_pip("list","--format", "json" )
    result_json = json.loads(result)
    package_to_version = {}
    for entry in result_json:
        name = entry["name"]
        version = entry["version"]
        package_to_version[name] = version
    return package_to_version


def is_installed(package:str):
    output = _call_pip("show", package)
    if output == "":
        return False
    else:
        return True

