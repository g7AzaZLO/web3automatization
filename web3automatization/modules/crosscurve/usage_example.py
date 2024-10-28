from web3automatization.classes.chain import chains
from web3automatization.classes.client import Client
from web3automatization.modules.crosscurve.logic import get_swap_route, get_estimate, create_swap_transaction, \
    send_crosscurve_swap_transaction

client = Client("private_key", chains["ethereum"].rpc, "proxy") #-  создаем клиента
route = get_swap_route(chains["optimism"], "USDT", chains["arbitrum"], "USDC.e", 1000, 0.1)["route"] #- ищем роут из оптимизм usdt в арбитрум usdc.e, количество 1000$, проскальзывание 0.1%
estimate = get_estimate(route) #- получаем estimate
swap_tnx = create_swap_transaction(client.public_key, route, estimate) #- формируем транзакцию
swap = send_crosscurve_swap_transaction(client, swap_tnx, estimate) #- подписываем и отправляем транзакцию