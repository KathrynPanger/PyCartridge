from pip_parser import parse_pip_show
from pip_interface import _call_pip
def test_format_pip_show():
    output =_call_pip("show", "pip")
    formatted_output = parse_pip_show(output)
    correct_keys = ['Name', 'Version', 'Summary', 'Home-page', 'Author', 'Author-email', 'License', 'Location', 'Requires', 'Required-by']
    assert list(formatted_output.keys()) == correct_keys