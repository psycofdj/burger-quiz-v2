import yaml
import os

def readFile(name):
    root = os.path.dirname(__file__)
    path = os.path.join(root, "resources", name)
    with open(path) as f:
        return yaml.safe_load(f)

data = {
    "nuggets": readFile("nuggets.yaml"),
    "selpoivre": readFile("selpoivre.yaml"),
    "menus": readFile("menus.yaml"),
    "menus-rouge": readFile("menus-rouge.yaml"),
    "addition": readFile("addition.yaml"),
}
