import json
from pathlib import Path

def loadjsondata(version, os_name)  -> dict:
    filepath = Path(f"{Path(__file__).parent}/Dice.json")
    return json.load(open(filepath, encoding="utf-8"))[version][os_name]