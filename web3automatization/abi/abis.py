import importlib.resources as pkg_resources
import json

ERC20_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "ERC20.json"))
CROSSCURVE_START_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "crosscurve_start.json"))
UNISWAP_ROUTER_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "uniswap_router.json"))
UNISWAP_QUOTER_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "uniswap_quoter.json"))
IOTEX_ABI = json.loads(pkg_resources.read_text("web3automatization.abi", "iotex_TokenCashierWithPayload.json"))