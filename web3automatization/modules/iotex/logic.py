from web3 import Web3
from web3automatization.abi.abis import IOTEX_ABI
from web3automatization.classes.client import Client
from web3automatization.modules.iotex.config import IOTEX_POLYGON_DEPOSIT_CONTRACT, POLYGON_NATIVE_POL


def get_deposit_in_iotex_from_polygon_transaction(client: Client, amount_in: float, token_address: str = POLYGON_NATIVE_POL):
    amount_in_scaled = amount_in * (10 ** client.get_decimals(token_address))
    contract = client.connection.eth.contract(address=Web3.to_checksum_address(IOTEX_POLYGON_DEPOSIT_CONTRACT), abi=IOTEX_ABI)
    params = (
        Web3.to_checksum_address(token_address),
        Web3.to_checksum_address(client.public_key),
        int(amount_in_scaled),
        b''
    )

    value = amount_in_scaled if token_address == POLYGON_NATIVE_POL else 0

    transaction = contract.functions.depositTo(
        *params
    ).build_transaction({
        'from': client.public_key,
        'value': value,
        'gas': client.connection.eth.estimate_gas({
            'to': IOTEX_POLYGON_DEPOSIT_CONTRACT,
            'from': client.public_key,
            'data': contract.encode_abi("depositTo", args=params),
            'value': value
        }),
        'gasPrice': client.connection.eth.gas_price,
        'nonce': client.get_nonce(client.public_key),
    })
    return transaction

def get_withdraw_in_polygon_from_iotex_transaction(client: Client, amount_in: float, token_address: str = POLYGON_NATIVE_POL):
    amount_in_scaled = amount_in * (10 ** client.get_decimals(token_address))
    contract = client.connection.eth.contract(address=Web3.to_checksum_address(IOTEX_POLYGON_DEPOSIT_CONTRACT), abi=IOTEX_ABI)
    params = (
        Web3.to_checksum_address(token_address),
        Web3.to_checksum_address(client.public_key),
        int(amount_in_scaled),
        b''
    )

    value = amount_in_scaled if token_address == POLYGON_NATIVE_POL else 0

    transaction = contract.functions.depositTo(
        *params
    ).build_transaction({
        'from': client.public_key,
        'value': value,
        'gas': client.connection.eth.estimate_gas({
            'to': IOTEX_POLYGON_DEPOSIT_CONTRACT,
            'from': client.public_key,
            'data': contract.encode_abi("depositTo", args=params),
            'value': value
        }),
        'gasPrice': client.connection.eth.gas_price,
        'nonce': client.get_nonce(client.public_key),
    })
    return transaction