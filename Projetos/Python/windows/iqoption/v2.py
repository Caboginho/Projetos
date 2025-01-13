from iqoptionapi.stable_api import IQ_Option
import time

class IQOptionApp:
    def __init__(self):
        self.api = None
        self.is_logged_in = False
        self.current_profile = "demo"

    def login(self, email, password):
        self.api = IQ_Option(email, password)
        self.is_logged_in, message = self.api.connect()
        if self.is_logged_in:
            print("Login bem-sucedido!")
        else:
            print(f"Erro ao fazer login: {message}")

    def switch_profile(self):
        if self.current_profile == "demo":
            self.api.change_balance("REAL")
            self.current_profile = "real"
        else:
            self.api.change_balance("PRACTICE")
            self.current_profile = "demo"
        print(f"Perfil alterado para: {self.current_profile}")

    def show_balance(self):
        balance = self.api.get_balance()
        print(f"Saldo atual ({self.current_profile}): ${balance:.2f}")

    def list_assets(self):
        if not self.api.check_connect():
            print("Conexão com a API foi perdida. Tentando reconectar...")
            self.api.connect()
            time.sleep(2)
        assets = self.api.get_all_open_time()  # Retorna todos os ativos disponíveis
        available_assets = {
            "binary": [],
            "digital": [],
            "crypto": [],
            "stocks": []
        }

        for market_type, items in assets.items():
            for asset, info in items.items():
                if info["open"]:
                    if market_type == "binary":
                        available_assets["binary"].append(asset)
                    elif market_type == "digital":
                        available_assets["digital"].append(asset)
                    elif market_type == "crypto":
                        available_assets["crypto"].append(asset)
                    elif market_type == "stocks":
                        available_assets["stocks"].append(asset)

        print("Ativos disponíveis:")
        for category, assets in available_assets.items():
            print(f"- {category.capitalize()}: {', '.join(assets) if assets else 'Nenhum ativo disponível'}")

    def binary_options(self, asset, amount, action, duration):
        if action.lower() not in ["buy", "sell"]:
            print("Ação inválida! Use 'buy' ou 'sell'.")
            return
        side = "call" if action.lower() == "buy" else "put"
        if not self.is_asset_open(asset, "binary"):
            print(f"O ativo {asset} não está aberto para transações binárias no momento.")
            return
        success, order_id = self.api.buy(amount, asset, side, duration)
        if success:
            print(f"Transação binária realizada com sucesso! ID: {order_id}")
        else:
            print("Erro ao realizar a transação binária.")

    def crypto_trading(self, asset, amount, action):
        if action.lower() not in ["buy", "sell"]:
            print("Ação inválida! Use 'buy' ou 'sell'.")
            return

        side = "call" if action.lower() == "buy" else "put"
        success, order_id = self.api.buy(amount, asset, side, 1)  # Exemplo de duração curta
        if success:
            print(f"Transação de cripto realizada com sucesso! ID: {order_id}")
        else:
            print("Erro ao realizar a transação de cripto.")

    def get_real_time_candles(self, asset, interval=1):
        print(f"Obtendo velas em tempo real para {asset} (intervalo de {interval} minuto(s))...")
        self.api.start_candles_stream(asset, interval, 10)  # Obtém 10 velas
        time.sleep(2)
        candles = self.api.get_realtime_candles(asset, interval)

        for candle_time, data in candles.items():
            print(f"{candle_time}: Open: {data['open']}, Close: {data['close']}, High: {data['max']}, Low: {data['min']}")

        self.api.stop_candles_stream(asset, interval)

    def get_current_price(self, asset):
        candles = self.api.get_candles(asset, 1, 1, time.time())
        current_price = candles[0]['close'] if candles else None
        print(f"Preço atual de {asset}: ${current_price:.2f}")
        return current_price

    def start(self):
        while True:
            #self.api.set_logging_level(1)
            print("\n=== Menu ===")
            print("1. Alternar perfil (demo/real)")
            print("2. Exibir saldo")
            print("3. Listar ativos disponíveis")
            print("4. Fazer transação binária")
            print("5. Fazer transação de cripto")
            print("6. Obter velas em tempo real")
            print("7. Obter preço atual de um ativo")
            print("8. Sair")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.switch_profile()
            elif choice == "2":
                self.show_balance()
            elif choice == "3":
                self.list_assets()
            elif choice == "4":
                asset = input("Digite o ativo (ex: EURUSD): ")
                amount = float(input("Digite o valor da transação: "))
                action = input("Digite a ação (buy/sell): ")
                duration = int(input("Digite a duração da posição (em minutos): "))
                self.binary_options(asset, amount, action, duration)
            elif choice == "5":
                asset = input("Digite o ativo (ex: BTCUSD): ")
                amount = float(input("Digite o valor da transação: "))
                action = input("Digite a ação (buy/sell): ")
                self.crypto_trading(asset, amount, action)
            elif choice == "6":
                asset = input("Digite o ativo (ex: EURUSD): ")
                interval = int(input("Digite o intervalo em minutos (ex: 1, 5): "))
                self.get_real_time_candles(asset, interval)
            elif choice == "7":
                asset = input("Digite o ativo (ex: EURUSD): ")
                self.get_current_price(asset)
            elif choice == "8":
                print("Encerrando o programa.")
                break
            else:
                print("Opção inválida. Tente novamente.")
                
    def is_asset_open(self, asset, market_type="binary"):
        open_assets = self.api.get_all_open_time()
        return open_assets[market_type].get(asset, {}).get("open", False)


if __name__ == "__main__":
    email = "george.uesc.cic@gmail.com"
    password = "@SenhaIqOption"

    app = IQOptionApp()
    app.login(email, password)

    if app.is_logged_in:
        app.start()
