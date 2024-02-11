from typing import Any

import yaml


def read_yaml_file(path: str) -> dict[str, Any]:
    with open(path, "r") as data:
        return yaml.safe_load(data)


def write_file(path: str, data: str) -> None:
    with open(path, "w") as file:
        file.write(data)
