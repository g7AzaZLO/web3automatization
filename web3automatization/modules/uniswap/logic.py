from web3automatization.classes.client import Client
from web3automatization.abi.abis import UNISWAP_QUOTER_ABI, UNISWAP_ROUTER_ABI
from web3automatization.modules.uniswap.config import QUOTER_ADDRESS, ROUTER_ADDRESS


def calculate_amount_in_with_slippage(client: Client, token_in: str, token_out: str, amount_out: float,
                                      sqrt_price_limit: int = 0, fee: int = 500, slippage=0.01) -> float | None:
    try:
        scaled_amount_out = int(amount_out * (10 ** client.get_decimals(token_out)))
        quoter = client.connection.eth.contract(address=QUOTER_ADDRESS, abi=UNISWAP_QUOTER_ABI)
        amount_in = quoter.functions.quoteExactOutputSingle(token_in, token_out, fee, scaled_amount_out,
                                                            sqrt_price_limit).call()
        amount_in_with_slippage = (amount_in + round(slippage * amount_in)) / (10 ** client.get_decimals(token_in))
        return amount_in_with_slippage
    except Exception as e:
        print(f"Error calculating amount in with slippage: {e}")
        return None


def uniswap_swap(client: Client, token_in: str, token_out: str, amount_out: float, amount_in_with_slippage: float,
                 sqrt_price_limit: int = 0, fee: int = 500, deadline: int = 2000000000):
    try:
        router = client.connection.eth.contract(address=ROUTER_ADDRESS, abi=UNISWAP_ROUTER_ABI)

        params = {
            'tokenIn': token_in,
            'tokenOut': token_out,
            'fee': fee,
            'recipient': client.public_key,
            'deadline': deadline,
            'amountOut': int(amount_out * (10 ** client.get_decimals(token_out))),
            'amountInMaximum': int(amount_in_with_slippage * (10 ** client.get_decimals(token_in))),
            'sqrtPriceLimitX96': sqrt_price_limit
        }

        transaction = {
            'from': client.public_key,
            'value': 0,
            'chainId': client.chain_id,
            'gasPrice': client.connection.eth.gas_price,
            'nonce': client.get_nonce()
        }

        transaction['gas'] = client.connection.eth.estimate_gas(transaction)

        swap_tx = router.functions.exactOutputSingle(params).build_transaction(transaction)
        tx_hash = client.send_transaction(swap_tx)

        print(f"Swap transaction hash: {tx_hash}")
        return tx_hash
    except Exception as e:
        print(f"Error executing uniswap swap transaction: {e}")
        return None
