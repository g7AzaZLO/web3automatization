[Читать на русском](README_RU.md)
# Documentation for the `web3automatization` Library

`web3automatization` is a library for simplifying interactions with EVM-based blockchain networks through `web3py`. It provides convenient methods for account management, transaction sending, ERC-20 token operations, and retrieving network information. The library also includes ready-made modules for interacting with various DeFi projects.

## Features

- Connect to various blockchain networks via RPC.
- Manage accounts using private keys.
- Send native and ERC-20 tokens.
- Perform `approve` operations for ERC-20 tokens.
- Retrieve balances and token information.
- Automatically estimate gas for transactions.

## Supported Projects
- CrossCurve
  - Cross-chain swaps
  - In-chain swaps
- Iotex
  - Bridge in Iotex from Polygon
  - Withdraw from Iotex to Polygon

## Installation

```bash
pip install web3automatization
```

## Usage

### Importing the Client

```python
from web3automatization import Client
```

### Initializing the Client

```python
private_key = "your private key"
rpc_url = "RPC server URL"

client = Client(private_key, rpc_url)
```

**Parameters:**

- `private_key` (str): Your account’s private key in hexadecimal format (with or without the '0x' prefix).
- `rpc_url` (str): URL of the blockchain network’s RPC server.
- `proxy` (str, optional): URL of the proxy server, if connection via proxy is needed.

**Example:**

```python
client = Client(
    private_key="0xc55af4055f19f388765840edee4e929efa333fb3b6a728979d1234567112c556",
    rpc="https://ethereum-rpc.publicnode.com",
    proxy="123.123.12.23:8080"
)
```

### Getting Account Balance

```python
balance = client.get_native_balance()
print(f"Account balance: {balance} ETH")
```

**Parameters:**

- `address` (str, optional): Address to check the balance for. If not specified, the client’s public key is used.

### Sending Native Token

```python
to_address = "recipient address"
amount = 0.1  # ETH

tx_hash = client.send_native(to_address, amount)
print(f"Transaction sent. Hash: {tx_hash}")
```

**Parameters:**

- `to_address` (str): Recipient address.
- `amount` (float): Amount to send in the network’s native token.

### Sending ERC-20 Tokens

```python
token_address = "ERC-20 token address"
to_address = "recipient address"
amount = 50  # Token amount

tx_hash = client.transfer_token(token_address, to_address, amount)
print(f"Transaction sent. Hash: {tx_hash}")
```

**Parameters:**

- `token_address` (str): Address of the ERC-20 token’s smart contract.
- `to_address` (str): Recipient address.
- `amount` (float): Amount of tokens to send.

### Performing an `approve` Operation

```python
token_address = "ERC-20 token address"
spender_address = "spender address"
amount = 1000  # Amount to approve

tx_hash = client.approve(token_address, spender_address, amount)
print(f"Approve transaction sent. Hash: {tx_hash}")
```

**Parameters:**

- `token_address` (str): Address of the ERC-20 token’s smart contract.
- `spender` (str): Address allowed to spend tokens.
- `amount` (float): Amount to approve.

### Performing a `permit approve` Operation

```python
token_address = "ERC-20 token address"
spender_address = "spender address"

tx_hash = client.permit_approve(token_address, spender_address)
print(f"Approve transaction sent. Hash: {tx_hash.hex()}")
```

**Parameters:**

- `token_address` (str): Address of the ERC-20 token’s smart contract.
- `spender` (str): Address allowed to spend tokens.

### Retrieving Token Information

#### Retrieving Token Decimals

```python
token_address = "ERC-20 token address"

decimals = client.get_decimals(token_address)
print(f"Token decimals: {decimals}")
```

**Parameters:**

- `token_address` (str): Token address.

#### Retrieving Token Allowance

```python
token_address = "ERC-20 token address"
spender_address = "spender address"

allowance = client.get_allowance(token_address, spender_address)
print(f"Token allowance: {allowance}")
```

**Parameters:**

- `token_address` (str): Token address.
- `spender` (str): Address allowed to spend tokens.

### Retrieving Account Nonce

```python
nonce = client.get_nonce()
print(f"Account nonce: {nonce}")
```

**Parameters:**

- `address` (str, optional): Account address. If not specified, the client’s public key is used.

### Retrieving Transaction Information

```python
tx_hash = "transaction hash in HexBytes"

receipt = client.get_transaction_receipt(tx_hash)
print(f"Transaction status: {receipt['status']}")
```

**Parameters:**

- `transaction_hash` (HexBytes): Transaction hash.

## Full `Client` Class Structure

```python
class Client:
    def __init__(self, private_key: str, rpc: str, proxy: str = None):
        # Client initialization

    def __del__(self) -> None:
        # Client destructor

    def __str__(self) -> str:
        # String representation of the client

    def get_nonce(self, address: str = None) -> int | None:
        # Retrieve nonce for an address

    def send_transaction(self, transaction: dict) -> str:
        # Sign and send transaction

    def send_native(self, to_address: str, amount: float) -> str:
        # Send ETH to a specified address

    def get_transaction_receipt(self, transaction_hash: str | HexBytes) -> dict:
        # Retrieve transaction information

    def get_native_balance(self, address: str = None) -> float | None:
        # Get ETH balance for an address

    def get_decimals(self, token_address: str) -> int | None:
        # Retrieve decimals for an ERC-20 token

    def get_allowance(self, token_address: str, spender: str) -> float | None:
        # Retrieve token allowance for an ERC-20 token

    def approve(self, token_address: str, spender: str, amount: float) -> str | None:
        # Perform approve operation for an ERC-20 token

    def transfer_token(self, token_address: str, to_address: str, amount: float) -> str | None:
        # Send ERC-20 token to a specified address
```

## Example of Full Usage

```python
from web3automatization import Client

# Initialize client
client = Client(
    private_key="0xc55af4055f19f388765840edee4e929efa333fb3b6a728979d1234567112c556",
    rpc="https://ethereum-rpc.publicnode.com",
    proxy="123.123.12.23:8080"
)

# Retrieve balance
balance = client.get_native_balance()
print(f"Balance: {balance} ETH")

# Send 0.05 ETH to another address
to_address = "0xRecipientAddressHere"
tx_hash = client.send_native(to_address, 0.05)
print(f"ETH sent. Transaction hash: {tx_hash}")

# Retrieve token information
token_address = "0xTokenAddressHere"
decimals = client.get_decimals(token_address)
print(f"Token decimals: {decimals}")

# Send 100 tokens to another address
tx_hash = client.transfer_token(token_address, to_address, 100)
print(f"Tokens sent. Transaction hash: {tx_hash}")

# Perform approve for 500 tokens
spender_address = "0xSpenderAddressHere"
tx_hash = client.approve(token_address, spender_address, 500)
print(f"Approve completed. Transaction hash: {tx_hash}")

# Retrieve allowance
allowance = client.get_allowance(token_address, spender_address)
print(f"Allowance for spender: {allowance}")
```

## Example Usage of CrossCurve Module

### Import the Module

```python
from web3automatization import Client, chains
from web3automatization.modules.crosscurve.logic import get_swap_route, get_estimate, create_swap_transaction, send_crosscurve_swap_transaction
```

### Finding the Route

```python
chain_in = chains["optimism"]
token_in = "USDT"
chain_out = chains["arbitrum"]
token_out = "USDC.e"
amount = 1000
slippage = 0.1

route = get_swap_route(chain_in, token_in, chain_out, token_out, amount, slippage)["route"]
```

You can also use the address of the token 

```Python
route = get_swap_route(chains["optimism"], "USDT", chains["arbitrum"], "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8", 1000, 0.1)["route"]
```

**Parameters:**

- `chain_in` (Chain): Chain object for the swap’s origin.
- `token_in` (str): Name of the token to be swapped from.
- `chain_out` (Chain): Chain object for the swap’s destination.
- `token_out` (str): Name of the token to be swapped to.
- `amount` (float): Amount to be swapped.
- `slippage` (float): Slippage percentage.

**Resulting Route:**

```commandline
1000 USDT from Optimism to USDC.e on Arbitrum with max slippage of 0.1%
```

### Getting Transaction Estimate

```python
estimate = get_estimate(route)
```

**Parameters:**

- `route` (list): Route obtained from `get_swap_route`.

### Creating the Swap Transaction

```python
swap_txn = create_swap_transaction(sender, route, estimate, client)
```

**Parameters:**

- `sender` (str): Address from which the transaction will be sent.
- `route` (list): Transaction path from `get_swap_route()`.
- `estimate` (dict): Estimate obtained from `get_estimate`.
- `client` (Client, optional): Client object to use the client’s proxy.

### Signing and Sending the Swap Transaction

```python
swap = send_crosscurve_swap_transaction(client, swap_txn, estimate)
```

**Parameters:**

- `client` (Client): Client object to sign the transaction.
- `swap_txn` (dict): Swap transaction created with `create_swap_transaction()`.
- `estimate` (dict): Transaction estimate from `get_estimate()`.

---

## Complete Usage

```python
from web3automatization.classes.chain import chains
from web3automatization.classes.client import Client
from web3automatization.modules.crosscurve.logic import get_swap_route, get_estimate, create_swap_transaction, send_crosscurve_swap_transaction

client = Client("0x...", chains["ethereum"].rpc, "123.123.123.12:8080")  # Initialize client
route = get_swap_route(chains["optimism"], "USDT", chains["arbitrum"], "USDC.e", 1000, 0.1)["route"]  # Find route from Optimism USDT to Arbitrum USDC.e, amount 1000, slippage 0.1%
estimate = get_estimate(route)  # Get estimate
swap_txn = create_swap_transaction(client.public_key, route, estimate)  # Create transaction
swap = send_crosscurve_swap_transaction(client, swap_txn, estimate)  # Sign and send transaction
```

## Example Usage of Iotex Module

### Import the Module

```python
import time
from web3automatization.classes.chain import chains
from web3automatization.modules.iotex.config import IOTEX_POLYGON_DEPOSIT_CONTRACT, IOTEX_WITHDRAW_CONTRACT
from web3automatization.modules.iotex.logic import get_deposit_in_iotex_from_polygon_transaction, \
    get_withdraw_in_polygon_from_iotex_transaction
from web3automatization.classes.client import Client
```

### Bridge in Iotex

```python
usdt_in_pol = "0xc2132d05d31c914a87c6611c10748aeb04b58e8f"
pol_usdt_in_iotex = "0x3cdb7c48e70b854ed2fa392e21687501d84b3afc"

client = Client("0x...", chains["polygon"].rpc)
client.approve(usdt_in_pol, IOTEX_POLYGON_DEPOSIT_CONTRACT, 5)
time.sleep(10)
print(client.send_transaction(get_deposit_in_iotex_from_polygon_transaction(client, 5, usdt_in_pol)))
```

### Withdraw from Iotex

```python
client = Client("0x...", chains["iotex"].rpc)
client.approve(pol_usdt_in_iotex, IOTEX_WITHDRAW_CONTRACT, 5)
time.sleep(10)
print(client.send_transaction(get_withdraw_in_polygon_from_iotex_transaction(client, 5, pol_usdt_in_iotex)))
```

## Conclusion

The library provides a simple and intuitive interface for interacting with EVM chains. It simplifies common operations and can be extended to support additional functionality as needed.

If you have suggestions for improvements or find any issues, please open an issue or pull request on the project’s repository.

*From sybils to sybils*

G7[telegram]: https://t.me/g7team_en
