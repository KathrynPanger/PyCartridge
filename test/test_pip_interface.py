from pip_interface import uninstall, is_installed, get_info, get_all_packages, install, _call_pip, get_version
import inspect
import pytest
import contextlib
from pip_parser import parse_pip_show
from fixtures import start_without_pandas, start_with_pandas, start_with_new_pandas, install_pandas_new, uninstall_pandas
import time


def test_call_pip(start_with_pandas):
    output = _call_pip("show", "pandas")
    package_info = parse_pip_show(output)
    correct_keys = ['Name', 'Version', 'Summary', 'Home-page', 'Author', 'Author-email', 'License', 'Location',
                    'Requires', 'Required-by']
    assert list(package_info.keys()) == correct_keys
    print(package_info)

def test_install_pandas(start_without_pandas):
    with pytest.raises(NameError):
        df = pandas.DataFrame()
    with pytest.raises(ModuleNotFoundError):
        import pandas
    install(package="pandas", constraints=["==2.1.1"])
    assert get_version("pandas") == "2.1.1"
    import pandas
    assert inspect.ismodule(pandas)


def test_uninstall_pandas(start_with_pandas):
    # Make sure pandas is installed
    # Fail the test if pandas is in namespace before import
    with pytest.raises(NameError):
        assert inspect.ismodule(pandas)
    # Fail the test if pandas is a module before import
    with pytest.raises(AssertionError):
        pandas = 5
        assert inspect.ismodule(pandas)
    # Try to remove the variable "pandas" from the namespace
    # even though its hopefully not there
    with contextlib.suppress(NameError):
        del pandas
    # Import pandas and make sure it's a module
    import pandas
    assert inspect.ismodule(pandas)

    # uninstall pandas and remove it from namespace
    uninstall("pandas")

    # Check that pandas is removed from namespace
    with pytest.raises(NameError):
        assert inspect.ismodule(pandas)
    # Check that pandas removed from installed packages
    assert "pandas" not in get_all_packages()


def test_uninstall_pandas_as_pd(start_with_pandas):
    import pandas as pd
    uninstall("pandas", reference_names=["pd"])
    with pytest.raises(ImportError):
        import pandas as pd
    with pytest.raises(NameError):
        assert inspect.ismodule(pd)



def test_is_installed_pandas_true(start_with_pandas):
    import pandas
    # Fail the test if pandas is not installed and imported
    assert inspect.ismodule(pandas)
    # Collect the tested function's output
    pandas_installed = is_installed("pandas")
    # Assess the output
    assert pandas_installed

def test_is_installed_pandas_false(start_without_pandas):
    # Make sure pandas is not installed
    with pytest.raises(ModuleNotFoundError):
        import pandas
    pandas_installed = is_installed("pandas")
    assert not pandas_installed


def test_get_info_pandas_not_installed(start_without_pandas):
    # check that pandas is not installed
    with pytest.raises(ModuleNotFoundError):
        import pandas
    # calling get_info should raise an exception
    with pytest.raises(ModuleNotFoundError):
        get_info("pandas")


@pytest.mark.parametrize('start_with_pandas', ["2.0.0"], indirect=True)
def test_get_info_versioned_pandas_is_installed(start_with_pandas):
    # get output of tested function
    output = get_info("pandas")
    # check for correct keys
    correct_keys = ['Name', 'Version', 'Summary', 'Home-page', 'Author', 'Author-email', 'License', 'Location',
                    'Requires', 'Required-by']
    assert list(output.keys()) == correct_keys
    # check correct version installed, visible in output
    assert output["Version"] == "2.0.0"
    # uninstall pandas again for next test
    uninstall("pandas")


def test_get_version_pandas_not_installed(start_without_pandas):
    # calling get_info should raise an exception
    with pytest.raises(ModuleNotFoundError):
        get_version("pandas")


@pytest.mark.parametrize('start_with_pandas', ["2.0.0"], indirect=True)
def test_get_version_versioned_pandas_installed(start_with_pandas):
    version = get_version("pandas")
    # test function
    assert version == "2.0.0"
    # uninstall pandas for next test
    uninstall("pandas")


def test_install_old_versioned_pandas(start_without_pandas):
    if is_installed("pandas"):
        uninstall("pandas")
    with pytest.raises(ModuleNotFoundError):
        import pandas
    install(package="pandas", constraints=["==2.0.0"])
    assert is_installed("pandas")
    import pandas
    assert inspect.ismodule(pandas)
    uninstall("pandas")


