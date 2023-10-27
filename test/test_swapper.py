import pytest

from swapper import Swapper
from pip_interface import install, uninstall, get_version


def test_swap_pandas(start_with_pandas):
    # Check version of pandas
    get_version("pandas")
    assert get_version("pandas") == "2.1.1"

    # use swapper to swap to pandas 2.0.0
    swapper = Swapper(package="pandas",
                      constraints=["==2.0.0"])
    with swapper:
        # Get new version number to verify swap success
        assert get_version("pandas") == "2.0.0"
    # check old version is back upon swapper exit
    assert get_version("pandas") == "2.1.1"


def test_swap_to_resolve_dependency_conflict():
    # Check none of three conflicting packages already installed
    with pytest.raises(ModuleNotFoundError):
        import datamakerkpanger882 as data_maker
        import topngetterkpanger882 as top_n_getter
        import listmakerkpanger882 as list_maker
    #