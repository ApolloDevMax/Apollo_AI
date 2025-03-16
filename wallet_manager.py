from web3 import Web3

# Подключение к сети Binance Smart Chain (BSC)
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# Проверяем подключение
if web3.is_connected():
    print("✅ Подключено к Binance Smart Chain")
else:
    print("❌ Ошибка подключения к сети BSC")

# Адрес кошелька (замени на свой)
WALLET_ADDRESS = "0xC56024688047c67c94BeF35822Fb1CB18a1854a1"

# Функция проверки баланса


def get_balance():
    balance = web3.eth.get_balance(WALLET_ADDRESS)
    balance_bnb = web3.from_wei(balance, 'ether')
    print(f"💰 Баланс кошелька: {balance_bnb} BNB")
    return balance_bnb


if __name__ == "__main__":
    get_balance()
