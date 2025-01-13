from iqoptionapi.stable_api import IQ_Option
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from table_updater import TableUpdater  # Importa a classe auxiliar para gerenciar a tabela
class IQOptionApp:
    def __init__(self, root):
        self.api = None
        self.username = None
        self.table_updater = None  # Inicializa o gerenciador de tabela
        self.table = []
        
        self.root = root
        self.root.title("IQ Option - Login e Alternar Perfis")

        # Etiquetas e campos para login
        tk.Label(root, text="Email:").grid(row=0, column=0, pady=5)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.grid(row=0, column=1, pady=5)

        tk.Label(root, text="Senha:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Caixa de seleção para lembrar login e senha
        self.remember_var = tk.BooleanVar()
        self.remember_check = tk.Checkbutton(root, text="Lembrar Login e Senha", variable=self.remember_var)
        self.remember_check.grid(row=2, column=0, columnspan=2, pady=5)

        # Botão de login
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=1, pady=10)

        # Botão de logoff
        self.logout_button = tk.Button(root, text="Logoff", command=self.logout, state="disabled")
        self.logout_button.grid(row=3, column=1, columnspan=1, pady=10)

        # Etiquetas para informações do usuário
        self.user_info = tk.Label(root, text="", font=("Arial", 12))
        self.user_info.grid(row=4, column=0, columnspan=2, pady=10)

        # Botão para alternar perfis
        self.profile_button = tk.Button(root, text="Alternar Perfil", command=self.toggle_profile, state="disabled")
        self.profile_button.grid(row=5, column=0, columnspan=2, pady=10)
       
        # Quadro para tabela
        self.table_frame = tk.Frame(root)
        self.table_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Configurar a tabela (Treeview)
        self.table = ttk.Treeview(root, columns=("Ativo", "Valor", "Estado da Vela", "Indicadores"), show="headings")
        self.table.grid(row=3, column=0, columnspan=2)

        # Configurar cabeçalhos da tabela
        self.table.heading("Ativo", text="Ativo")
        self.table.heading("Valor", text="Valor")
        self.table.heading("Estado da Vela", text="Estado da Vela")
        self.table.heading("Indicadores", text="Indicadores")

        # Ajustar largura das colunas
        self.table.column("Ativo", width=100)
        self.table.column("Valor", width=100)
        self.table.column("Estado da Vela", width=150)
        self.table.column("Indicadores", width=150)
        
        # Carregar credenciais salvas
        self.load_credentials()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Erro", "Preencha o email e a senha.")
            return

        self.api = IQ_Option(email, password)
        success, message = self.api.connect()
        if success:
            self.logout_button.config(state="normal")
            self.login_button.config(state="disabled")
            self.username = email
            self.update_user_info()
            self.profile_button.config(state="normal")
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")

            # Salvar credenciais, se a opção "Lembrar" estiver marcada
            if self.remember_var.get():
                self.save_credentials(email, password)
            else:
                self.clear_saved_credentials()

            # Iniciando o Atualizador da tabela
            self.start_table_updater()
        else:
            messagebox.showerror("Erro", f"Falha ao realizar login: {message}")

    def update_user_info(self):
        if self.api:
            profile_type = self.api.get_balance_mode()
            balance = self.api.get_balance()
            self.user_info.config(text=f"Usuário: {self.username}\nPerfil: {profile_type.title()}\nSaldo: ${balance:.2f}")

    def toggle_profile(self):
        if self.api:
            current_profile = self.api.get_balance_mode()
            new_profile = "REAL" if current_profile == "PRACTICE" else "PRACTICE"
            self.api.change_balance(new_profile)
            self.update_user_info()
            messagebox.showinfo("Sucesso", f"Perfil alterado para: {new_profile.title()}")

    def save_credentials(self, email, password):
        with open("credentials.txt", "w") as file:
            file.write(f"{email}\n{password}")

    def load_credentials(self):
        if os.path.exists("credentials.txt"):
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                if len(lines) == 2:
                    email = lines[0].strip()
                    password = lines[1].strip()
                    self.email_entry.insert(0, email)
                    self.password_entry.insert(0, password)
                    self.remember_var.set(True)

    def clear_saved_credentials(self):
        if os.path.exists("credentials.txt"):
            os.remove("credentials.txt")

    def start_table_updater(self):
        # Inicializa e inicia a atualização da tabela
        self.table_updater = TableUpdater(self.api, self.table_frame)
        self.table_updater.start_updating()

    def logout(self):
        if self.api:
            self.login_button.config(state="normal")
            self.api.disconnect()
            self.api = None
            self.user_info.config(text="")
            self.profile_button.config(state="disabled")
            self.table_updater.stop_updating()  # Para a atualização da tabela
            messagebox.showinfo("Logoff", "Você foi desconectado com sucesso!")

    def create_trade_window(self):
        # Nova janela para realizar compra ou venda
        trade_window = tk.Toplevel(self.root)
        trade_window.title("Executar Operações")

        tk.Label(trade_window, text="Ativo:").grid(row=0, column=0, pady=5)
        self.asset_entry = tk.Entry(trade_window, width=30)
        self.asset_entry.grid(row=0, column=1, pady=5)

        tk.Label(trade_window, text="Valor:").grid(row=1, column=0, pady=5)
        self.value_entry = tk.Entry(trade_window, width=30)
        self.value_entry.grid(row=1, column=1, pady=5)

        tk.Label(trade_window, text="Direção:").grid(row=2, column=0, pady=5)
        self.direction_var = tk.StringVar(value="CALL")
        tk.Radiobutton(trade_window, text="Compra (CALL)", variable=self.direction_var, value="CALL").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(trade_window, text="Venda (PUT)", variable=self.direction_var, value="PUT").grid(row=3, column=1, sticky="w")

        tk.Label(trade_window, text="Duração (em minutos):").grid(row=4, column=0, pady=5)
        self.duration_entry = tk.Entry(trade_window, width=30)
        self.duration_entry.grid(row=4, column=1, pady=5)

        tk.Button(trade_window, text="Executar", command=self.execute_trade).grid(row=5, column=0, columnspan=2, pady=10)

    def execute_trade(self):
        asset = self.asset_entry.get()
        value = float(self.value_entry.get()) if self.value_entry.get().isdigit() else 0
        direction = self.direction_var.get()
        duration = int(self.duration_entry.get()) if self.duration_entry.get().isdigit() else 1

        if not asset or value <= 0 or duration <= 0:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        try:
            expiration_time = duration * 60  # Converter minutos para segundos
            success, trade_id = self.api.buy(value, asset, direction, expiration_time)
            if success:
                messagebox.showinfo("Sucesso", f"Operação executada com sucesso! ID: {trade_id}")
            else:
                messagebox.showerror("Erro", "Falha ao executar a operação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar a operação: {e}")

def load_assets_from_file():
    try:
        with open("ativos.txt", "r") as file:
            assets = [line.strip() for line in file.readlines()]
        print("Ativos carregados:", assets)  # Debug para ver os ativos lidos
        return assets
    except FileNotFoundError:
        print("Erro: O arquivo 'ativos.txt' não foi encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao carregar ativos: {e}")
        return []

    
if __name__ == "__main__":
    root = tk.Tk()
    app = IQOptionApp(root)
   
    if not app.api:
        print("API não conectada. Não é possível iniciar o atualizador de tabela.")
        
    assets = load_assets_from_file()  # Carrega os ativos do arquivo
    if not assets:
        print("Nenhum ativo carregado. Verifique o arquivo 'ativos.txt'.")
            
        
    # Inicializa o atualizador de tabela
    table_updater = TableUpdater(api= app.api,table_frame=assets)
    table_updater.populate_table(assets)  # Preenche a tabela com os ativos
    table_updater.start_updating()
    
    root.mainloop()

