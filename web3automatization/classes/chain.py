import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


class Chain:
    def __init__(self, name: str, chain_id: int, rpc: str, native_token: str, alternative_rpc: list[str]):
        self.name = name
        self.id = chain_id
        self.rpc = rpc
        self.native_token = native_token
        self.alternative_rpc = alternative_rpc  # Массив альтернативных RPC-серверов, если первый недоступен
        self.current_rpc_index = 0

    def set_rpc_url(self, url: str) -> bool:
        self.rpc = url
        return True

    def switch_to_alternative_rpc(self) -> bool:
        if self.current_rpc_index < len(self.alternative_rpc):
            self.rpc = self.alternative_rpc[self.current_rpc_index]
            self.current_rpc_index += 1
            return True
        else:
            logger.warning(f"No more alternative RPCs available for chain {self.name}")
            return False

    @classmethod
    def get(cls, identifier: str | int) -> dict | None:
        """
        Получает информацию о сети по названию или идентификатору сети.

        :param identifier: Название сети (str) или идентификатор сети (int).
        :return: Словарь с информацией о сети, если найдена, иначе None.
        """
        for chain in chains.values():
            if (isinstance(identifier, str) and chain.name.lower() == identifier.lower()) or \
                    (isinstance(identifier, int) and chain.id == identifier):
                return {
                    "name": chain.name,
                    "chain_id": chain.id,
                    "rpc": chain.rpc,
                    "native_token": chain.native_token,
                    "alternative_rpc": chain.alternative_rpc
                }
        logger.warning("Chain not found.")
        return None


chains = {
    "ethereum": Chain(
        'ethereum',
        1,
        "https://ethereum-rpc.publicnode.com",
        "ETH",
        ["https://eth.llamarpc.com", "https://rpc.payload.de", "https://1rpc.io/eth"]),
    "bsc": Chain(
        'bsc',
        56,
        "https://binance.llamarpc.com",
        "BNB",
        ["https://bsc.meowrpc.com", "https://bsc-rpc.publicnode.com", "https://bsc.meowrpc.com"]),
    "arbitrum": Chain(
        'arbitrum',
        42161,
        "https://arbitrum.llamarpc.com",
        "ETH",
        ["https://arbitrum.drpc.org", "https://1rpc.io/arb", "https://arb-pokt.nodies.app",
         "https://arbitrum.meowrpc.com"]),
    "base": Chain(
        'base',
        8453,
        "https://base.llamarpc.com",
        "ETH",
        ["https://base-rpc.publicnode.com", "https://1rpc.io/base", "https://base.meowrpc.com"]),
    "avalanche": Chain(
        'avalance',
        43114,
        "https://avalanche-c-chain-rpc.publicnode.com",
        "AVAX",
        ["https://avalanche.drpc.org", "https://1rpc.io/avax/c", "https://avalanche-c-chain-rpc.publicnode.com"]),
    "polygon": Chain(
        'polygon',
        137,
        "https://polygon.llamarpc.com",
        "MATIC",
        ["https://1rpc.io/matic", "https://polygon.drpc.org", "https://polygon-bor-rpc.publicnode.com"]),
    "optimism": Chain(
        'optimism',
        10,
        "https://optimism-rpc.publicnode.com",
        "ETH",
        ["https://1rpc.io/op", "https://optimism.llamarpc.com", "https://optimism.drpc.org"]),
    "gnosis": Chain(
        'gnosis',
        100,
        "https://gnosis-rpc.publicnode.com",
        "XDAI",
        ["https://gnosis-rpc.publicnode.com", "https://gnosis-pokt.nodies.app", "https://1rpc.io/gnosis"]),
    "linea": Chain(
        'linea',
        59144,
        "https://linea-rpc.publicnode.com",
        "ETH",
        ["https://rpc.linea.build", "https://linea.blockpi.network/v1/rpc/public"]),
    "blast": Chain(
        'blast',
        81457,
        "https://blast-rpc.publicnode.com",
        "ETH",
        ["https://blast.drpc.org", "https://rpc.blast.io"]),
    "mantle": Chain(
        'mantle',
        5000,
        "https://1rpc.io/mantle",
        "MNT",
        ["https://rpc.mantle.xyz", "https://mantle-mainnet.public.blastapi.io", "https://1rpc.io/mantle"]),
    "taiko": Chain(
        'taiko',
        167000,
        "https://rpc.ankr.com/taiko",
        "ETH",
        ["https://taiko-mainnet.rpc.porters.xyz/taiko-public", "https://taiko-rpc.publicnode.com",
         "https://taiko.drpc.org"]),
    "iotex": Chain(
        "iotex",
        4689,
        "https://rpc.ankr.com/iotex",
        "IOTX",
        ["https://babel-api.mainnet.iotex.one", "https://babel-api.mainnet.iotex.io", "https://babel-api.fastblocks.io"]
    )
}

poa_list = [
    chains["polygon"].id,
    chains['bsc'].id,
    chains["gnosis"].id,
]
