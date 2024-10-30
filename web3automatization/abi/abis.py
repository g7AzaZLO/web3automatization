import importlib.resources as pkg_resources
import json

ERC20_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "ERC20.json"))
CROSSCURVE_START_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "crosscurve_start.json"))
