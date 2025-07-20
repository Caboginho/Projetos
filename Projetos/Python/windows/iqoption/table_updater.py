import threading
import time
from tkinter import ttk


class TableUpdater:
    def __init__(self, api, table_frame):
        self.api = api
        self.table_frame = table_frame
        self.stop_event = threading.Event()
        self.table = []
        self.matrix = []  # Para armazenar os dados da tabela
        self.create_table()
        

    def create_table(self):
        # Cria uma tabela no frame fornecido
        self.table = ttk.Treeview(
            self.table_frame, columns=("Ativo", "Valor", "Estado da Vela", "Indicadores"), show="headings"
        )
        self.table.heading("Ativo", text="Ativo")
        self.table.heading("Valor", text="Valor")
        self.table.heading("Estado da Vela", text="Estado da Vela")
        self.table.heading("Indicadores", text="Indicadores")
        self.table.pack(fill="both", expand=True)

    def update_table(self):
        while not self.stop_event.is_set():
            try:
                self.matrix.clear()  # Limpa os dados antes de atualizar
                ativos = self.api.get_all_open_time()  # Obtém os ativos disponíveis
                for ativo, info in ativos.items():
                    if info["open"]:  # Verifique se o ativo está aberto para negociação
                        valor = self.get_asset_value(ativo)
                        estado_vela = self.get_candle_status(ativo)
                        indicadores = self.get_indicators(ativo)
                        # Adiciona os dados à matriz
                        self.matrix.append([ativo, valor, estado_vela, indicadores])
                # Atualiza a tabela com os novos dados
                self.display_table()
            except Exception as e:
                print(f"Erro ao atualizar tabela: {e}")
            time.sleep(3)  # Aguarde 3 segundos antes de atualizar novamente

    def start_updating(self):
        # Inicia um thread para atualizar a tabela
        self.update_thread = threading.Thread(target=self.update_table, daemon=True)
        self.update_thread.start()

    def stop_updating(self):
        # Para um thread de atualização
        self.stop_event.set()
        self.update_thread.join()

    def get_asset_value(self, ativo):
        try:
            info = self.api.get_financial_information(ativo)
            print(f"Dados recebidos para {ativo}: {info}")
            return info.get("price", "N/A")
        except Exception as e:
            print(f"Erro ao obter valor do ativo {ativo}: {e}")
            return "Erro"

    def get_candle_status(self, ativo):
        try:
            velas = self.api.get_candles(ativo, 60, 1, time.time())  # Velas de 1 minuto
            if velas:
                return "Alta" if velas[0]["close"] > velas[0]["open"] else "Baixa"
            return "Indefinido"
        except Exception as e:
            print(f"Erro ao obter estado da vela para {ativo}: {e}")
            return "Erro"

    def get_indicators(self, ativo):
        try:
            # Exemplos de indicadores para futuro desenvolvimento
            return "RSI: 70 | SMA: 200"
        except Exception as e:
            print(f"Erro ao obter indicadores para {ativo}: {e}")
            return "Erro"

    def display_table(self):
        # Remove todas as entradas atuais na tabela
        self.table.delete(*self.table.get_children())
        # Insira os dados da matriz na tabela
        for data in self.matrix:
            self.table.insert("", "end", values=data)
    
    def populate_table(self, assets):
        for asset in assets:
            value = self.get_asset_value(asset)
            candle_status = self.get_candle_status(asset)
            indicators = self.get_indicators(asset)  # Método fictício, ajuste conforme necessário
            self.table.insert("", "end", values=(asset, value, candle_status, indicators))

