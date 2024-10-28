from typing import List, Tuple, Any
from web3 import Account


def generate_account(nums: int) -> list[list[str, str, str]]:
    accounts = []
    for i in range(nums):
        print("------------------------------")
        Account.enable_unaudited_hdwallet_features()
        account, mnemonic = Account.create_with_mnemonic()
        print(f"Адрес вашего кошелька: {account.address}")
        print(f"Сид фраза вашего кошелька: {mnemonic}")
        print(f"Приватный ключ вашего кошелька: {account.key.hex()}")
        accounts.append([account.address, mnemonic, "0x" + account.key.hex()])
    return accounts


def mnemonic_to_private_key(mnemonics: list) -> list:
    """
    Преобразует список мнемонических фраз в список приватных ключей.

    :param mnemonics: Список мнемонических фраз.
    :return: Список приватных ключей, соответствующих каждой мнемонической фразе.
    """
    Account.enable_unaudited_hdwallet_features()  # Включаем поддержку неаудированных функций
    private_key_list = []
    for memo in mnemonics:
        account = Account.from_mnemonic(memo)  # Создаем аккаунт на основе мнемонической фразы
        private_key_list.append(account._private_key.hex())  # Получаем приватный ключ и добавляем в список
    return private_key_list
