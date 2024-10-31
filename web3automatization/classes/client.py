import logging
from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
from web3automatization.abi.abis import ERC20_ABI
from web3automatization.classes.chain import poa_list

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, private_key: str, rpc: str, proxy: str = None):
        """
        Инициализирует клиента с подключением к RPC через прокси и настройкой аккаунта на основе приватного ключа.

        :param private_key: Приватный ключ в шестнадцатеричном формате (с или без префикса '0x').
        :param rpc: URL RPC-сервера.
        :param proxy: URL прокси-сервера (например '312.123.43.43:8080').
        :raises ConnectionError: Если не удается подключиться к RPC.
        """
        self.logger = logger
        self.logger.info(f"Initializing client with proxy {proxy}")

        self.rpc = rpc
        self.proxy = proxy

        # Настройка провайдера с учетом прокси
        if self.proxy:
            provider = HTTPProvider(self.rpc, {"proxies": {"http": self.proxy}})
        else:
            provider = HTTPProvider(self.rpc)

        self.connection = Web3(provider)

        # Проверка подключения к RPC
        if not self.connection.is_connected():
            self.logger.error(f"Failed to connect to the RPC at {self.rpc}")
            raise ConnectionError(f"Failed to connect to the RPC at {self.rpc}")

        self.chain_id = self.connection.eth.chain_id
        if self.chain_id in poa_list:
            self.logger.info(f"Client is connected to a PoA chain (chain_id={self.chain_id})")
            self.logger.info("Client is set middleware for PoA")
            self.connection.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        # Обработка приватного ключа
        self.private_key = bytes.fromhex(private_key[2:] if private_key.startswith('0x') else private_key)
        self.account = self.connection.eth.account.from_key(self.private_key)
        self.public_key = self.account.address

        self.logger.info(f"Client initialized with public_key={self.public_key}")

    def __del__(self) -> None:
        """
        Сообщает, что клиент был удален.
        """
        self.logger.info(f"Client with public_key={self.public_key} was deleted")

    def __str__(self) -> str:
        """
        Возвращает строковое представление клиента.
        """
        return (
            f"Client(\n"
            f"  public_key={self.public_key},\n"
            f"  private_key={'0x' + self.private_key.hex()},\n"
            f"  rpc={self.rpc},\n"
            f"  proxy={self.proxy},\n"
            f")"
        )

    def get_nonce(self, address: str = None) -> int | None:
        """
        Получает текущий nonce для учетной записи.

        :param address: Адрес учетной записи. Если не указан, используется публичный ключ клиента.
        :return: Nonce для учетной записи.
        """
        if address is None:
            address = self.public_key
        self.logger.info(f"Getting nonce for address {address}")
        try:
            nonce = self.connection.eth.get_transaction_count(address)
            self.logger.info(f"Nonce for address {address}: {nonce}")
            return nonce
        except Exception as e:
            self.logger.warning(f"Error occurred while getting nonce for address {address}: {e}")
            return None

    def send_transaction(self, transaction: dict) -> str:
        """
        Подписывает и отправляет транзакцию в сеть, возвращая её хеш.

        :param transaction: Словарь с данными транзакции.
        :return: Хеш отправленной транзакции.
        """
        self.logger.info(f"Sending transaction: {transaction}")
        signed_transaction = self.account.sign_transaction(transaction)
        tx_hash = self.connection.eth.send_raw_transaction(signed_transaction.raw_transaction)
        self.logger.info(f"Transaction sent with hash {tx_hash.hex()}")
        return "0x"+tx_hash.hex()

    def send_native(self, to_address: str, amount: float) -> str | None:
        """
        Отправляет ETH на указанный адрес с автоматической оценкой газа.

        :param to_address: Адрес получателя.
        :param amount: Сумма для отправки в ETH.
        :return: Хеш транзакции.
        """
        self.logger.info(f"Sending {amount} ETH to {to_address}")

        # Приведение amount к минимальным единицам (wei)
        value = self.connection.to_wei(amount, 'ether')

        # Получение nonce для транзакции
        nonce = self.get_nonce()

        # Создание транзакции без указания газа
        transaction = {
            'to': Web3.to_checksum_address(to_address),
            'value': value,
            'nonce': nonce,
            'chainId': self.chain_id
        }

        # Автоматическая оценка газа и получение текущей цены газа
        try:
            estimated_gas = self.connection.eth.estimate_gas(transaction)
            gas_price = self.connection.eth.gas_price

            # Добавление оценки газа и цены газа в транзакцию
            transaction['gas'] = estimated_gas
            transaction['gasPrice'] = gas_price

            # Подписывание и отправка транзакции
            tx_hash = self.send_transaction(transaction)
            self.logger.info(f"ETH transaction sent with hash {tx_hash}")
            return tx_hash
        except Exception as e:
            self.logger.warning(f"Error occurred while sending ETH: {e}")
            return None

    def get_transaction_receipt(self, transaction_hash: str | HexBytes) -> dict:
        """
        Получает информацию о транзакции на основе её хеша.

        :param transaction_hash: Хеш транзакции.
        :return: Словарь с информацией о транзакции.
        """
        self.logger.info(f"Getting transaction receipt for hash {transaction_hash}")
        return self.connection.eth.get_transaction_receipt(transaction_hash)

    def get_native_balance(self, address: str = None) -> float | None:
        """
        Получает баланс аккаунта в ETH.

        :param address: Адрес для проверки баланса. Если не указан, используется публичный ключ клиента.
        :return: Баланс аккаунта в ETH.
        """
        if address is None:
            address = self.public_key
        self.logger.info(f"Getting native balance for address {address}")
        try:
            balance_wei = self.connection.eth.get_balance(address)
            balance_eth = self.connection.from_wei(balance_wei, 'ether')
            self.logger.info(f"Native balance for address {address}: {balance_eth} ETH")
            return balance_eth
        except Exception as e:
            self.logger.warning(f"Error occurred while getting native balance for address {address}: {e}")
            return None

    def get_decimals(self, token_address: str) -> int | None:
        """
        Получает количество десятичных знаков токена.

        :param token_address: Адрес токена.
        :return: Количество десятичных знаков токена.
        """
        self.logger.info(f"Getting decimals for token {token_address}")
        try:
            contract = self.connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )
            decimals = contract.functions.decimals().call()
            self.logger.info(f"Decimals for token {token_address}: {decimals}")
            return decimals
        except Exception as e:
            self.logger.warning(f"Error occurred while getting decimals for token {token_address}: {e}")
            return None

    def get_allowance(self, token_address: str, spender: str) -> float | None:
        """
        Получает текущий лимит (allowance) токенов, который владелец разрешил spender.

        :param token_address: Адрес смарт-контракта токена (ERC-20).
        :param spender: Адрес, которому разрешено тратить токены.
        :return: Лимит токенов в формате float с учетом decimals.
        """
        self.logger.info(f"Getting allowance for token {token_address} and spender {spender}")
        try:
            decimals = self.get_decimals(token_address)
            contract = self.connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )
            allowance = contract.functions.allowance(
                self.public_key,
                Web3.to_checksum_address(spender)
            ).call()
            allowance_float = allowance / (10 ** decimals)
            self.logger.info(f"Allowance for token {token_address}: {allowance_float}")
            return allowance_float
        except Exception as e:
            self.logger.warning(f"Error occurred while getting allowance for token {token_address}: {e}")
            return None

    def approve(self, token_address: str, spender: str, amount: float) -> str | None:
        """
        Выполняет approve транзакцию, позволяя spender расходовать до amount токенов от имени владельца.

        :param token_address: Адрес смарт-контракта токена (ERC-20).
        :param spender: Адрес, которому разрешено тратить токены.
        :param amount: Количество токенов для одобрения (в формате float).
        :return: Хеш транзакции.
        """
        try:
            self.logger.info(f"Approving {amount} tokens for spender {spender} on contract {token_address}")

            # Создание объекта контракта
            contract = self.connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )

            # Получение количества знаков после запятой (decimals)
            decimals = contract.functions.decimals().call()

            # Приведение amount к минимальным единицам токена
            scaled_amount = int(amount * (10 ** decimals))

            # Nonce для транзакции
            nonce = self.get_nonce()

            # Оценка газа для транзакции
            estimated_gas = contract.functions.approve(
                Web3.to_checksum_address(spender),
                scaled_amount
            ).estimate_gas({'from': self.public_key})

            # Получение текущей цены газа
            gas_price = self.connection.eth.gas_price

            # Создание транзакции для вызова метода approve
            transaction = contract.functions.approve(
                Web3.to_checksum_address(spender),
                scaled_amount
            ).build_transaction({
                'from': self.public_key,
                'nonce': nonce,
                'gas': estimated_gas,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            })

            # Подписывание и отправка транзакции
            tx_hash = self.send_transaction(transaction)
            self.logger.info(f"Approve transaction sent with hash {tx_hash}")
            return tx_hash
        except Exception as e:
            self.logger.warning(f"Error occurred during approve: {e}")
            return None

    def permit_approve(self, token_address: str, spender: str) -> str | None:
        """
        Выполняет permit approve транзакцию, позволяя spender расходовать бесконечно токенов от имени владельца.

        :param token_address: Адрес смарт-контракта токена (ERC-20).
        :param spender: Адрес, которому разрешено тратить токены.
        :return: Хеш транзакции.
        """
        try:
            self.logger.info(f"Permit approving tokens for spender {spender} on contract {token_address}")

            # Создание объекта контракта
            contract = self.connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )

            # Приведение amount к минимальным единицам токена
            permit_amount = 2 ** 256 - 1

            # Nonce для транзакции
            nonce = self.get_nonce()

            # Оценка газа для транзакции
            estimated_gas = contract.functions.approve(
                Web3.to_checksum_address(spender),
                permit_amount
            ).estimate_gas({'from': self.public_key})

            # Получение текущей цены газа
            gas_price = self.connection.eth.gas_price

            # Создание транзакции для вызова метода approve
            transaction = contract.functions.approve(
                Web3.to_checksum_address(spender),
                permit_amount
            ).build_transaction({
                'from': self.public_key,
                'nonce': nonce,
                'gas': estimated_gas,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            })

            # Подписывание и отправка транзакции
            tx_hash = self.send_transaction(transaction)
            self.logger.info(f"Permit approve transaction sent with hash {tx_hash}")
            return tx_hash
        except Exception as e:
            self.logger.warning(f"Error occurred during approve: {e}")
            return None

    def transfer_token(self, token_address: str, to_address: str, amount: float) -> str | None:
        """
        Отправляет ERC-20 токены на указанный адрес.

        :param token_address: Адрес смарт-контракта токена (ERC-20).
        :param to_address: Адрес получателя.
        :param amount: Сумма для отправки в формате float.
        :return: Хеш транзакции.
        """
        self.logger.info(f"Transferring {amount} of token {token_address} to {to_address}")

        try:
            # Создание объекта контракта
            contract = self.connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=ERC20_ABI
            )

            # Получение количества знаков после запятой (decimals)
            decimals = contract.functions.decimals().call()

            # Приведение amount к минимальным единицам токена
            scaled_amount = int(amount * (10 ** decimals))

            # Nonce для транзакции
            nonce = self.get_nonce()

            # Оценка газа для транзакции
            estimated_gas = contract.functions.transfer(
                Web3.to_checksum_address(to_address),
                scaled_amount
            ).estimate_gas({'from': self.public_key})

            # Получение текущей цены газа
            gas_price = self.connection.eth.gas_price

            # Создание транзакции
            transaction = contract.functions.transfer(
                Web3.to_checksum_address(to_address),
                scaled_amount
            ).build_transaction({
                'from': self.public_key,
                'nonce': nonce,
                'gas': estimated_gas,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            })

            # Подписывание и отправка транзакции
            tx_hash = self.send_transaction(transaction)
            self.logger.info(f"Token transfer transaction sent with hash {tx_hash}")
            return tx_hash
        except Exception as e:
            self.logger.warning(f"Error occurred during token transfer: {e}")
            return None
