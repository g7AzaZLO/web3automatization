import time
from web3automatization.classes.chain import chains
from web3automatization.modules.iotex.config import IOTEX_POLYGON_DEPOSIT_CONTRACT, IOTEX_WITHDRAW_CONTRACT
from web3automatization.modules.iotex.logic import get_deposit_in_iotex_from_polygon_transaction, \
    get_withdraw_in_polygon_from_iotex_transaction
from web3automatization.classes.client import Client

usdt_in_pol = "0xc2132d05d31c914a87c6611c10748aeb04b58e8f"
pol_usdt_in_iotex = "0x3cdb7c48e70b854ed2fa392e21687501d84b3afc"

client = Client("0x...", chains["polygon"].rpc)
client.approve(usdt_in_pol, IOTEX_POLYGON_DEPOSIT_CONTRACT, 5)
time.sleep(10)
print(client.send_transaction(get_deposit_in_iotex_from_polygon_transaction(client, 5, usdt_in_pol)))
client = Client("0x...", chains["iotex"].rpc)
client.approve(pol_usdt_in_iotex, IOTEX_WITHDRAW_CONTRACT, 5)
time.sleep(10)
print(client.send_transaction(get_withdraw_in_polygon_from_iotex_transaction(client,5, pol_usdt_in_iotex)))
