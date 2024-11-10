import requests
from web3 import Web3
from web3automatization.abi.abis import CROSSCURVE_START_ABI
from web3automatization.classes.chain import Chain
from web3automatization.classes.client import Client
from config import crosscurve_tokens, UNIFIED_ROUTER_V2


def find_token(chain: Chain, ticker_or_address: str) -> dict | None:
    """
    Находит токен по объекту сети и тикеру или адресу токена.

    :param chain: Объект сети.
    :param ticker_or_address: Тикер токена или адрес контракта.
    :return: Словарь с данными токена, если найден, иначе None.
    """
    for token in crosscurve_tokens:
        if token['chain'].lower() == chain.name.lower() and (
                token['ticker'].lower() == ticker_or_address.lower() or
                token['address'].lower() == ticker_or_address.lower()):
            return token
    return None


def get_swap_route(chain_in: Chain, token_in_identifier: str, chain_out: Chain, token_out_identifier: str,
                   amount_in: float, slippage: float, client: Client = None) -> dict | None:
    """
    Проверяет маршрут обмена из указанного входного токена на указанный выходной токен.

    :param chain_in: Объект сети, в которой находится входной токен.
    :param token_in_identifier: Тикер или адрес входного токена.
    :param chain_out: Объект сети, в которой находится выходной токен.
    :param token_out_identifier: Тикер или адрес выходного токена.
    :param amount_in: Количество входного токена для обмена.
    :param slippage: Допустимое проскальзывание.

    :param client: Опциональный объект клиента с прокси-настройками.
    :return: Словарь с информацией о маршруте, если найден подходящий маршрут, иначе None.
    """
    try:
        # Поиск данных входного и выходного токенов
        token_in = find_token(chain_in, token_in_identifier)
        token_out = find_token(chain_out, token_out_identifier)

        if not token_in or not token_out:
            print("Не удалось найти один или оба токена в списке.")
            return None

        print(f"Checking swap route from {token_in['address']} to {token_out['address']}")

        # Масштабирование amountIn с учетом decimals
        decimals_in = token_in.get('decimals')
        amount_in_scaled = str(int(amount_in * (10 ** decimals_in)))

        url = "https://api.crosscurve.fi/routing/scan"
        params = {
            "params": {
                "chainIdOut": chain_out.id,
                "tokenOut": token_out["address"],
                "chainIdIn": chain_in.id,
                "amountIn": amount_in_scaled,
                "tokenIn": token_in["address"]
            },
            "slippage": slippage
        }

        proxies = {
            "http": client.proxy
        } if client and client.proxy else None

        response = requests.post(url, json=params, proxies=proxies)

        if response.status_code == 200:
            data = response.json()
            if data and "amountOutWithoutSlippage" in data[0]:
                amount_out_raw = float(data[0]["amountOutWithoutSlippage"])
                decimals_out = token_out.get('decimals')
                amount_out = amount_out_raw / (10 ** decimals_out)
                total_fee = float(data[0].get("totalFee").get("amount"))

                print(f"SWAP ROUTE FOUND: in {amount_in} -> out {amount_out}")
                return {
                    "from_token": token_in["ticker"],
                    "from_chain": chain_in.name,
                    "to_token": token_out["ticker"],
                    "to_chain": chain_out.name,
                    "amount_in": amount_in,
                    "amount_out": amount_out,
                    "route": data[0],
                    "fee": total_fee
                }
            print("Response data is empty")
            return None
        print(f"Response status != 200: {response.status_code}")
        return None
    except Exception as e:
        print(f"Request error: {e}")
        return None


def get_estimate(route: list, client: Client = None) -> dict | None:
    """
    Отправляет запрос на получение оценки маршрута обмена.

    :param route: Словарь с данными лучшего маршрута.
    :param client: Опциональный объект клиента с прокси-настройками.
    :return: Словарь с оценкой маршрута или None в случае ошибки.
    """
    url = 'https://api.crosscurve.fi/estimate'
    headers = {
        "Content-Type": "application/json",
    }

    try:
        proxies = {
            "http": client.proxy
        } if client is not None and client.proxy else None

        response = requests.post(url, json=route, headers=headers, proxies=proxies)
        response.raise_for_status()
        estimate = response.json()
        return estimate
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
    return None


def create_swap_transaction(sender: str, routing: dict, estimate: dict,
                            client: Client = None) -> dict | None:
    """
    Создает транзакцию с использованием предоставленных параметров и отправляет запрос на создание транзакции.

    :param sender: Адрес отправителя.
    :param recipient: Адрес получателя.
    :param routing: Данные маршрутизации.
    :param estimate: Оценка маршрута.
    :param client: Опциональный объект клиента с прокси-настройками.
    :return: Словарь с данными сырой транзакции или None в случае ошибки.
    """
    if client is not None:
        sender = client.public_key

    url = 'https://api.crosscurve.fi/tx/create'
    headers = {
        "Content-Type": "application/json",
    }

    tx_create_params = {
        "from": sender,
        "recipient": sender,
        "routing": routing,
        "estimate": estimate,
    }

    try:
        proxies = {
            "http": client.proxy
        } if client is not None and client.proxy else None

        response = requests.post(url, json=tx_create_params, headers=headers, proxies=proxies)
        response.raise_for_status()
        raw_tx = response.json()
        return raw_tx
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
    return None


def send_crosscurve_swap_transaction(client: Client, raw_tx: dict, estimate: dict) -> str | None:
    """
    Выполняет транзакцию с использованием предоставленных данных.

    :param client: Объект клиента для подключения и отправки транзакции.
    :param raw_tx: Словарь с данными сырой транзакции.
    :param estimate: Словарь с оценкой маршрута.
    :return: Словарь с данными о завершенной транзакции или None в случае ошибки.
    """
    try:
        router = client.connection.eth.contract(address=Web3.to_checksum_address(raw_tx['to']),
                                                abi=CROSSCURVE_START_ABI)
        args = [
            list(raw_tx['args'][0]),
            list(raw_tx['args'][1]),
            [
                int(raw_tx['args'][2]['executionPrice']),
                int(raw_tx['args'][2]['deadline']),
                int(raw_tx['args'][2]['v']),
                Web3.to_bytes(hexstr=raw_tx['args'][2]['r']),
                Web3.to_bytes(hexstr=raw_tx['args'][2]['s'])
            ]
        ]

        value = int(raw_tx['value']) + int(estimate['executionPrice'])
        transaction = router.functions.start(
            *args
        ).build_transaction({
            'from': client.public_key,
            'value': value,
            'gas': client.connection.eth.estimate_gas({
                'to': UNIFIED_ROUTER_V2,
                'from': client.public_key,
                'data': router.encodeABI("start", args=args),
                'value': value
            }),
            'gasPrice': client.connection.eth.gas_price,
            'nonce': client.get_nonce(client.public_key),
        })

        print("Try to send swap transaction")
        hash = client.send_transaction(transaction)

        print(f"Transaction successful with hash: {hash}")
        return hash

    except Exception as e:
        print(f"Error occurred while executing transaction: {e}")
        return None
