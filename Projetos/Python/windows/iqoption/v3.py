import threading
import time
from iqoptionapi.stable_api import IQ_Option
import pandas as pd
import matplotlib.pyplot as plt

class WoodiesCCI:
    def __init__(self, api, asset):
        self.api = api
        self.asset = asset
        self.data = pd.DataFrame(columns=["time", "open", "close", "min", "max", "volume"])
        self.running = True

    def fetch_candles(self, interval=60, count=50):
        """Busca as últimas velas do ativo e atualiza o DataFrame."""
        candles = self.api.get_candles(self.asset, interval, count, time.time())
        df = pd.DataFrame(candles)
        df = df.rename(columns={
            "from": "time",
            "open": "open",
            "close": "close",
            "min": "min",
            "max": "max",
            "volume": "volume"
        })
        df["time"] = pd.to_datetime(df["time"], unit="s")
        self.data = df[["time", "open", "close", "min", "max", "volume"]]

    def calculate_woodies_cci(self, period=14):
        """Calcula o Woodies CCI baseado nos dados disponíveis."""
        typical_price = (self.data["close"] + self.data["min"] + self.data["max"]) / 3
        self.data["typical_price"] = typical_price
        self.data["sma"] = typical_price.rolling(window=period).mean()
        self.data["mean_deviation"] = typical_price.rolling(window=period).apply(lambda x: abs(x - x.mean()).mean())

        self.data["cci"] = (typical_price - self.data["sma"]) / (0.015 * self.data["mean_deviation"])
        self.data["base_cci"] = self.data["cci"].rolling(window=34).mean()

    def plot_woodies_cci(self):
        """Plota o gráfico do Woodies CCI em tempo real."""
        plt.ion()  # Modo interativo para atualizações em tempo real
        fig, ax = plt.subplots(figsize=(10, 6))
        while self.running:
            self.fetch_candles()  # Atualiza os dados
            self.calculate_woodies_cci()  # Calcula o indicador
            
            ax.clear()
            ax.plot(self.data["time"], self.data["cci"], label="CCI Principal", color="blue")
            ax.plot(self.data["time"], self.data["base_cci"], label="CCI Base", color="orange")
            ax.axhline(100, color="green", linestyle="--", label="Sobrecompra")
            ax.axhline(-100, color="red", linestyle="--", label="Sobrevenda")
            ax.axhline(0, color="black", linestyle="-", linewidth=0.5)

            ax.legend(loc="upper left")
            ax.set_title(f"Woodies CCI - {self.asset}")
            ax.set_xlabel("Tempo")
            ax.set_ylabel("CCI")
            plt.pause(1/4)  # Atualização a cada 1 segundo

        plt.ioff()
        plt.show()

    def stop(self):
        """Para o gráfico."""
        self.running = False

class IQOptionApp:
    def __init__(self):
        self.api = None
        self.is_logged_in = False

    def login(self, email, password):
        """Login na API."""
        self.api = IQ_Option(email, password)
        self.is_logged_in, message = self.api.connect()
        if self.is_logged_in:
            print("Login bem-sucedido!")
        else:
            print(f"Erro ao fazer login: {message}")

    def change_balance(self, balance_type):
        """Altera o tipo de conta."""
        def _change_balance():
            if balance_type.upper() in ["PRACTICE", "REAL"]:
                self.api.change_balance(balance_type.upper())
                print(f"Conta alterada para: {balance_type}")
            else:
                print("Tipo de conta inválido. Use PRACTICE ou REAL.")

        threading.Thread(target=_change_balance).start()

    def get_balance(self):
        """Obtém o saldo atual."""
        def _get_balance():
            balance = self.api.get_balance()
            print(f"Saldo atual: ${balance:.2f}")

        threading.Thread(target=_get_balance).start()

    def list_assets(self):
        """Lista os ativos disponíveis para negociação."""
        def _list_assets():
            assets = self.api.get_all_open_time()
            if not assets:
                print("Não foi possível obter os ativos disponíveis.")
                return

            print("\nAtivos disponíveis:")
            for market_type, items in assets.items():
                print(f" - {market_type.capitalize()}:")
                for asset, info in items.items():
                    if info["open"]:
                        print(f"   * {asset}")

        threading.Thread(target=_list_assets).start()

    def make_transaction(self, amount, asset, action, duration):
        """Realiza uma transação binária."""
        def _make_transaction():
            """print(f"Tentando realizar uma transação:")
            print(f" - Ativo: {asset}")
            print(f" - Valor: {amount}")
            print(f" - Ação: {action}")
            print(f" - Duração: {duration}")"""

            # Verifique se o ativo está aberto para negociação
            assets = self.api.get_all_open_time()
            if not assets.get("binary", {}).get(asset, {}).get("open", False):
                print(f"Erro: O ativo {asset} não está disponível para negociação no momento.")
                return

            # Determinar o tipo de ação
            side = "call" if action.lower() == "buy" else "put"
            success, order_id = self.api.buy(amount, asset, side, duration)

            if success:
                print(f"Transação realizada com sucesso! ID: {order_id}")
            else:
                print("Erro ao realizar a transação. Verifique os parâmetros fornecidos ou as regras da API.")

        threading.Thread(target=_make_transaction).start()


    def get_candles(self, asset, timeframe, count, endtime):
        """Obtém velas (candlesticks) de um ativo."""
        def _get_candles():
            candles = self.api.get_candles(asset, timeframe, count, endtime)
            print(f"\nVelas para o ativo {asset}:")
            for candle in candles:
                print(f" - De {candle['from']} até {candle['to']} | Abertura: {candle['open']} | Fechamento: {candle['close']}")

        threading.Thread(target=_get_candles).start()

    def check_connect(self):
        """Verifica a conexão com a API."""
        def _check_connect():
            if self.api.check_connect():
                print("Conexão ativa com a API.")
            else:
                print("Conexão perdida. Tentando reconectar...")
                self.api.connect()

        threading.Thread(target=_check_connect).start()
        
    def start_woodies_thread(self, asset):
        """Inicia o gráfico Woodies CCI em uma thread."""
        woodies_cci = WoodiesCCI(self.api, asset)
        thread = threading.Thread(target=woodies_cci.plot_woodies_cci)
        thread.start()
        return woodies_cci, thread

def menu():
    """Menu para interação com os métodos."""
    app = IQOptionApp()
    email = "george.uesc.cic@gmail.com"
    password = "@SenhaIqOption"

    app.login(email, password)

    if not app.is_logged_in:
        print("Não foi possível realizar o login.")
        return

    while True:
        print("\n=== MENU ===")
        print("1. Alterar conta (demo/real)")
        print("2. Ver saldo")
        print("3. Listar ativos")
        print("4. Fazer transação binária")
        print("5. Obter velas de um ativo")
        print("6. Verificar conexão")
        print("7. WoodiesCCI")
        print("8. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            balance_type = input("Digite o tipo de conta (PRACTICE ou REAL): ")
            app.change_balance(balance_type)
        elif choice == "2":
            app.get_balance()
        elif choice == "3":
            app.list_assets()
        elif choice == "4":
            asset = input("Digite o ativo (ex.: EURUSD): ")
            amount = float(input("Digite o valor da transação: "))
            action = input("Digite a ação (buy/sell): ")
            duration = int(input("Digite a duração em minutos: "))
            app.make_transaction(amount, asset, action, duration)
        elif choice == "5":
            asset = input("Digite o ativo (ex.: EURUSD): ")
            timeframe = int(input("Digite o período das velas (em segundos): "))
            count = int(input("Digite o número de velas: "))
            endtime = int(time.time())  # Pega o timestamp atual
            app.get_candles(asset, timeframe, count, endtime)
        elif choice == "6":
            app.check_connect()
        elif choice == "7":
            if app.api.check_connect():
                asset = input("Digite o ativo (ex.: EURUSD): ")
                woodies_cci, thread = app.start_woodies_thread(asset)
                try:
                    while True:
                        time.sleep(3)
                except KeyboardInterrupt:
                    print("\nEncerrando...")
                    woodies_cci.stop()
                    thread.join()
            else:
                print("Erro ao conectar ao IQ Option.")
        elif choice == "8":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
