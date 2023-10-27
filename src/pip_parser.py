from collections.abc import Mapping


def parse_pip_show(output: str) -> Mapping[str:str]:
    corpus = output.split("\n")
    package_to_version = {}
    for item in corpus:
        line = item.split(": ", maxsplit=1)
        if len(line)<=1:
            continue
        name = line[0]
        version = line[1]
        package_to_version[name] = version
    return package_to_version