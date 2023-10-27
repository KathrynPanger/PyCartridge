import pytest
from pip_interface import is_installed, uninstall, get_version, install

test_package = "pandas"
new_version = "2.1.1"
old_version = "2.0.0"

# Setup Functions
@pytest.fixture
def install_pandas_new():
    install(test_package, [f"=={new_version}"])
    return

@pytest.fixture
def install_pandas_old():
    install(test_package, [f"=={old_version}"])
    return

# Teardown Functions
@pytest.fixture
def uninstall_pandas():
    yield
    uninstall(test_package)

# Setup Teardown Functions (Buggy)

@pytest.fixture
def start_with_new_pandas(install_pandas_new, uninstall_pandas):
    pass

@pytest.fixture
def start_with_pandas(request):
    try:
        version = request.param if hasattr(request, "param") else "2.1.1"
        install(package="pandas", constraints=[f"=={version}"])
        yield
    finally:
        uninstall("pandas")
        assert not is_installed("pandas")
@pytest.fixture
def start_without_pandas():
    try:
        if is_installed("pandas"):
            uninstall("pandas")
        yield
    finally:
        uninstall("pandas")
        assert not is_installed("pandas")