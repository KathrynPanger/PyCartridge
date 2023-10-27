from dataclasses import dataclass
from typing import Optional
import inspect
from pip_interface import install, uninstall, get_version, is_installed

# TODO check if old version is same as new version before install, warn
@dataclass
class Swapper():
    package: str
    constraints: list[str]
    reference_names: Optional[list[str]] = None

    def __enter__(self):
        # Check if package is already installed
        if is_installed(self.package):
            # If so, capture the version
            self.was_installed = True
            self.original_version = get_version(self.package)
            uninstall(package=self.package, reference_names=self.reference_names)
        # Install it with the swapped version
        install(package=self.package, constraints=self.constraints)
        if self.reference_names is not None:
            for name in self.reference_names:
                exec(f"import {self.package} as {self.name}")
        else:
            exec(f"import {self.package}")

    def __exit__(self, exception_type, exception_value, traceback):
        # Get the version of the swapped install
        self.swap_version = get_version(self.package)
        # Check if uninstall is needed
        if self.original_version != self.swap_version:
            # Uninstall the package
            uninstall(self.package)
            # Re-install the version previously being used, if captured
            install(self.package, constraints=f"=={self.original_version}")