# This code is used to validate or deserialize data comming from a yaml file 
# By Ed Scrimaglia

from pydantic import ValidationError
import json
import yaml
from data_model import *

# Reading data template to validate
try:
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file.read())
    data_json = json.dumps(data, indent=2)
except FileNotFoundError as err:
    print (f"{err=}")

# Data template validation
try:
    dev = DataModel.model_validate_json(data_json)
    validation = dev.model_dump_json(indent=2)
    print (f"Validation: {data_json == validation}")
except ValidationError as err:
    print (f"{err=}")
