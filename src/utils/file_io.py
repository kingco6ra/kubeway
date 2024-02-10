import yaml

from models.services import Service


def get_services_from_file(path: str) -> list[Service]:
    with open(path, "r") as data:
        return [Service.from_dict(item) for item in yaml.safe_load(data)]


def write_configuration_file(path: str, configuration: str) -> None:
    with open(path, "w") as file:
        file.write(configuration)
