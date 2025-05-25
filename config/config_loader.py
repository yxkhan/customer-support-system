#This file is to load the .yaml configuration and enable the package to be used as a module.

import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config