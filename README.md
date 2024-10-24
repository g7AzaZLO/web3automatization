# Документация к библиотеке `web3automatization`

`web3automatization` — это библиотека для упрощения взаимодействия с блокчейн-сетями на основе EVM через web3py. Она предоставляет удобные методы для управления аккаунтом, отправки транзакций, работы с токенами ERC-20 и получения информации из сети.

## Возможности

- Подключение к различным блокчейн-сетям через RPC.
- Управление аккаунтом на основе приватного ключа.
- Отправка ETH и ERC-20 токенов.
- Выполнение операций `approve` для токенов ERC-20.
- Получение балансов и информации о токенах.
- Автоматическая оценка газа для транзакций.

## Установка зависимостей

```bash
pip install -r requirements.txt
```
## Использование

### Импорт клиента

```python
from client import Client
```

### Инициализация клиента

```python
private_key = "ваш приватный ключ"
rpc_url = "URL RPC-сервера"

client = Client(private_key, rpc_url)
```

**Параметры:**

- `private_key` (str): Приватный ключ вашего аккаунта в шестнадцатеричном формате (с или без префикса '0x').
- `rpc_url` (str): URL RPC-сервера блокчейн-сети.
- `proxy` (str, необязательно): URL прокси-сервера, если требуется подключение через прокси.

**Пример:**

```python
client = Client(
    private_key="0xc55af4055f19f388765840edee4e929efa333fb3b6a728979d1234567112c556",
    rpc="https://ethereum-rpc.publicnode.com"
    proxy="123.123.12.23:8080"
)
```

### Получение баланса аккаунта

```python
balance = client.get_native_balance()
print(f"Баланс аккаунта: {balance} ETH")
```

**Параметры:**

- `address` (str, необязательно): Адрес для проверки баланса. Если не указан, используется публичный ключ клиента.

### Отправка нативного токена

```python
to_address = "адрес получателя"
amount = 0.1  # ETH

tx_hash = client.send_native(to_address, amount)
print(f"Транзакция отправлена. Хеш: {tx_hash.hex()}")
```

**Параметры:**

- `to_address` (str): Адрес получателя.
- `amount` (float): Сумма для отправки в нативном токене сети.

### Отправка ERC-20 токенов

```python
token_address = "адрес токена ERC-20"
to_address = "адрес получателя"
amount = 50  # Количество токенов

tx_hash = client.transfer_token(token_address, to_address, amount)
print(f"Транзакция отправлена. Хеш: {tx_hash.hex()}")
```

**Параметры:**

- `token_address` (str): Адрес смарт-контракта токена ERC-20.
- `to_address` (str): Адрес получателя.
- `amount` (float): Количество токенов для отправки.

### Выполнение операции `approve`

```python
token_address = "адрес токена ERC-20"
spender_address = "адрес, которому разрешено тратить токены"
amount = 1000  # Количество токенов для одобрения

tx_hash = client.approve(token_address, spender_address, amount)
print(f"Транзакция approve отправлена. Хеш: {tx_hash.hex()}")
```

**Параметры:**

- `token_address` (str): Адрес смарт-контракта токена ERC-20.
- `spender` (str): Адрес, которому разрешено тратить токены.
- `amount` (float): Количество токенов для одобрения.

### Получение информации о токене

#### Получение количества десятичных знаков (decimals)

```python
token_address = "адрес токена ERC-20"

decimals = client.get_decimals(token_address)
print(f"Decimals токена: {decimals}")
```

**Параметры:**

- `token_address` (str): Адрес токена.

#### Получение одобренного лимита токенов (`allowance`)

```python
token_address = "адрес токена ERC-20"
spender_address = "адрес, которому разрешено тратить токены"

allowance = client.get_allowance(token_address, spender_address)
print(f"Allowance токенов: {allowance}")
```

**Параметры:**

- `token_address` (str): Адрес токена.
- `spender` (str): Адрес, которому разрешено тратить токены.

### Получение номера транзакции(nonce) аккаунта

```python
nonce = client.get_nonce()
print(f"Nonce аккаунта: {nonce}")
```

**Параметры:**

- `address` (str, необязательно): Адрес учетной записи. Если не указан, используется публичный ключ клиента.

### Получение информации о транзакции

```python
tx_hash = "хеш транзакции в HexBytes"

receipt = client.get_transaction_receipt(tx_hash)
print(f"Статус транзакции: {receipt['status']}")
```

**Параметры:**

- `transaction_hash` (HexBytes): Хеш транзакции.

## Полная структура класса `Client`

```python
class Client:
    def __init__(self, private_key: str, rpc: str, proxy: str = None):
        # Инициализация клиента

    def __del__(self) -> None:
        # Деструктор клиента

    def __str__(self) -> str:
        # Строковое представление клиента

    def get_nonce(self, address: str = None) -> int | None:
        # Получение nonce для адреса

    def send_transaction(self, transaction: dict) -> HexBytes:
        # Подписание и отправка транзакции

    def send_native(self, to_address: str, amount: float) -> HexBytes:
        # Отправка ETH на указанный адрес

    def get_transaction_receipt(self, transaction_hash: HexBytes) -> dict:
        # Получение информации о транзакции

    def get_native_balance(self, address: str = None) -> float | None:
        # Получение баланса в ETH для адреса

    def get_decimals(self, token_address: str) -> int | None:
        # Получение decimals для токена ERC-20

    def get_allowance(self, token_address: str, spender: str) -> float | None:
        # Получение allowance для токена ERC-20

    def approve(self, token_address: str, spender: str, amount: float) -> HexBytes | None:
        # Выполнение операции approve для токена ERC-20

    def transfer_token(self, token_address: str, to_address: str, amount: float) -> HexBytes | None:
        # Отправка токена ERC-20 на указанный адрес
```

## Пример полного использования

```python
from client import Client

# Инициализация клиента
client = Client(
    private_key="0xc55af4055f19f388765840edee4e929efa333fb3b6a728979d1234567112c556",
    rpc="https://ethereum-rpc.publicnode.com"
    proxy="123.123.12.23:8080"
)

# Получение баланса
balance = client.get_native_balance()
print(f"Баланс: {balance} ETH")

# Отправка 0.05 ETH на другой адрес
to_address = "0xRecipientAddressHere"
tx_hash = client.send_eth(to_address, 0.05)
print(f"ETH отправлен. Хеш транзакции: {tx_hash.hex()}")

# Получение информации о токене
token_address = "0xTokenAddressHere"
decimals = client.get_decimals(token_address)
print(f"Decimals токена: {decimals}")

# Отправка 100 токенов на другой адрес
tx_hash = client.transfer_token(token_address, to_address, 100)
print(f"Токены отправлены. Хеш транзакции: {tx_hash.hex()}")

# Выполнение approve на 500 токенов
spender_address = "0xSpenderAddressHere"
tx_hash = client.approve(token_address, spender_address, 500)
print(f"Approve выполнен. Хеш транзакции: {tx_hash.hex()}")

# Получение allowance
allowance = client.get_allowance(token_address, spender_address)
print(f"Allowance для spender: {allowance}")
```

---

## Заключение

Библиотека предоставляет простой и интуитивно понятный интерфейс для взаимодействия с EVM чейнами. Она упрощает выполнение часто используемых операций и может быть расширена для поддержки дополнительной функциональности в соответствии с вашими потребностями.

Если у вас есть предложения по улучшению или вы нашли ошибку, пожалуйста, создайте issue или pull request в репозитории проекта.

От сибилов - для сибилов
