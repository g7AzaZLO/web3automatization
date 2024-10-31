from web3automatization.classes.chain import chains
from web3automatization.classes.client import Client
from web3automatization.modules.uniswap.config import ROUTER_ADDRESS
from web3automatization.modules.uniswap.logic import calculate_amount_in_with_slippage, uniswap_swap

wmatic_address = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
usdс_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

client = Client("0x_pk", chains["polygon"].rpc) # подключаемся к полигону
client.approve(wmatic_address, ROUTER_ADDRESS, 1) # делаем апрув 1 wmatic

amount_out_with_slippage = calculate_amount_in_with_slippage(client, wmatic_address, usdс_address, 0.3) # полчаем цену. Сколько нужно отдать wmatic зв 1 usdc
print(uniswap_swap(client, wmatic_address, usdс_address, 0.3, amount_out_with_slippage)) # свапаем wmatic тобы получить 0.3 usdc
