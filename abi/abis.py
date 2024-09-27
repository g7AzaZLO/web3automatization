import json
import os

abi_path_erc20 = os.path.join(os.path.dirname(__file__), "ERC20.json")
with open(abi_path_erc20, "r") as file:
    ERC20_ABI = json.load(file)