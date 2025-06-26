import yaml

def carregar_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
