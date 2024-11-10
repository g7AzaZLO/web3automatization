import aiosqlite
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


async def init_db() -> None:
    """
    Инициализирует базу данных `web3automatization`, создавая таблицы `accounts`, `bybit`, `okx` и `proxies`, `bybit_address`, `okx_address`, если они не существуют.
    """
    async with aiosqlite.connect("web3automatization.db") as db:
        # Создание таблицы `accounts`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                private_key TEXT NOT NULL,      -- Приватный ключ
                public_key TEXT NOT NULL,       -- Публичный ключ
                proxy TEXT,                     -- Прокси
                okx_address TEXT,               -- Адрес вывода на биржу OKX
                bybit_address TEXT              -- Адрес вывода на биржу Bybit
            )
        """)

        # Создание таблицы `bybit`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bybit (
                bybit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL,          -- API-ключ для Bybit
                private_key TEXT NOT NULL       -- Приватный ключ для Bybit
            )
        """)

        # Создание таблицы `okx`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS okx (
                okx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL,          -- API-ключ для OKX
                private_key TEXT NOT NULL       -- Приватный ключ для OKX
                passphrase TEXT NOT NULL        -- Пароль для OKX
            )
        """)

        # Создание таблицы `proxies`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS proxies (
                proxy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT NOT NULL,            -- Прокси
                linked_wallet TEXT              -- Привязанный кошелек
            )
        """)

        # Создание таблицы `bybit_address`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bybit_address (
                bb_address TEXT PRIMARY KEY,
                public_key TEXT
            )
        """)

        # Создание таблицы `okx_address`
        await db.execute("""
            CREATE TABLE IF NOT EXISTS okx_address (
                okx_address TEXT PRIMARY KEY,
                public_key TEXT
            )
        """)
        await db.commit()
    logger.info("База данных `web3automatization` и таблицы проверены/созданы.")


async def add_okx_address(okx_address: str) -> bool:
    """
    Добавляет новый OKX-адрес в таблицу okx_address.

    :param okx_address: Строка с адресом OKX, который нужно добавить.
    :return: True, если адрес добавлен успешно; иначе False.
    """
    async with aiosqlite.connect("web3automatization.db") as db:
        try:
            await db.execute("INSERT INTO okx_address (okx_address) VALUES (?)", (okx_address,))
            await db.commit()
            logger.info(f"OKX-адрес {okx_address} успешно добавлен.")
            return True
        except aiosqlite.IntegrityError:
            logger.warning(f"OKX-адрес {okx_address} уже существует в таблице.")
            return False


async def add_bybit_address(bb_address: str) -> bool:
    """
    Добавляет новый Bybit-адрес в таблицу bybit_address.

    :param bb_address: Строка с адресом Bybit, который нужно добавить.
    :return: True, если адрес добавлен успешно; иначе False.
    """
    async with aiosqlite.connect("web3automatization.db") as db:
        try:
            await db.execute("INSERT INTO bybit_address (bb_address) VALUES (?)", (bb_address,))
            await db.commit()
            logger.info(f"Bybit-адрес {bb_address} успешно добавлен.")
            return True
        except aiosqlite.IntegrityError:
            logger.warning(f"Bybit-адрес {bb_address} уже существует в таблице.")
            return False


async def bind_wallet_to_any_unused_okx_address(public_key: str) -> str | None:
    """
    Привязывает кошелек (публичный ключ) к свободному адресу OKX.

    :param public_key: Публичный ключ кошелька, который нужно привязать.
    :return: Адрес OKX, к которому был привязан публичный ключ, если привязка успешна; иначе None.
    """
    async with aiosqlite.connect("web3automatization.db") as db:
        # Поиск свободного адреса OKX, где public_key равен NULL
        async with db.execute("SELECT okx_address FROM okx_address WHERE public_key IS NULL LIMIT 1") as cursor:
            row = await cursor.fetchone()

        if row:
            okx_address = row[0]

            # Обновляем таблицу okx_address, привязывая public_key к найденному адресу OKX
            await db.execute("UPDATE okx_address SET public_key = ? WHERE okx_address = ?", (public_key, okx_address))

            # Проверяем, есть ли этот public_key в таблице accounts
            async with db.execute("SELECT account_id FROM accounts WHERE public_key = ?", (public_key,)) as cursor:
                account = await cursor.fetchone()

            # Если запись существует, обновляем ее, добавляя привязанный okx_address
            if account:
                await db.execute("UPDATE accounts SET okx_address = ? WHERE public_key = ?", (okx_address, public_key))

            # Сохраняем изменения в базе данных
            await db.commit()

            logger.info(f"Кошелек с публичным ключом {public_key} привязан к OKX-адресу {okx_address}.")
            return okx_address
        else:
            logger.warning("Свободный OKX-адрес не найден.")
            return None


async def bind_wallet_to_any_unused_bybit_address(public_key: str) -> str | None:
    """
    Привязывает кошелек (публичный ключ) к свободному адресу Bybit.

    :param public_key: Публичный ключ кошелька, который нужно привязать.
    :return: Адрес Bybit, к которому был привязан публичный ключ, если привязка успешна; иначе None.
    """
    async with aiosqlite.connect("web3automatization.db") as db:
        async with db.execute("SELECT bb_address FROM bybit_address WHERE public_key IS NULL LIMIT 1") as cursor:
            row = await cursor.fetchone()

        if row:
            bybit_address = row[0]
            await db.execute("UPDATE bybit_address SET public_key = ? WHERE bb_address = ?",
                             (public_key, bybit_address))

            async with db.execute("SELECT account_id FROM accounts WHERE public_key = ?", (public_key,)) as cursor:
                account = await cursor.fetchone()

            if account:
                await db.execute("UPDATE accounts SET bybit_address = ? WHERE public_key = ?",
                                 (bybit_address, public_key))

            await db.commit()
            logger.info(f"Кошелек с публичным ключом {public_key} привязан к Bybit-адресу {bybit_address}.")
            return bybit_address
        else:
            logger.warning("Свободный Bybit-адрес не найден.")
            return None
