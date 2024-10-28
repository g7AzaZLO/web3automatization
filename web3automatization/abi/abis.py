import os
import sys
from pathlib import Path
from web3automatization.utils.read_utils import read_json

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, "abi")

ERC20_ABI = read_json(os.path.join(ABIS_DIR, "ERC20.json"))
CROSSCURVE_START_ABI = read_json(os.path.join(ABIS_DIR, "crosscurve_start.json"))
