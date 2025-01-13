import sqlite3
import psycopg2
class BancoDeDados:
    def __init__(self):
        self.conexao = sqlite3.connect('vendas.db')
        self.cursor = self.conexao.cursor()

    def executar(self, query, parametros=()):
        try:
            self.cursor.execute(query, parametros)
            self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")

    def consultar(self, query, parametros=()):
        try:
            self.cursor.execute(query, parametros)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao consultar: {e}")
            return []
    
    def enviar_notificacao(self, id_usuario, mensagem):
        self.executar(
            '''
            INSERT INTO notificacoes (id_usuario, mensagem, lida)
            VALUES (?, ?, 0)
            ''',
            (id_usuario, mensagem)
        )
    def executar_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conexao.commit()
        except Exception as e:
            self.conexao.rollback()
            print("Erro ao executar query:", e)

    def buscar(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print("Erro ao buscar dados:", e)
            return []

    def fechar(self):
        self.conexao.close()
    
    @staticmethod
    def inicializar_banco():
        conexao = sqlite3.connect('vendas.db')
        cursor = conexao.cursor()

        # Tabela usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('cliente', 'prestador'))
        )
        ''')

        # Tabela produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL,
            id_prestador INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('produto', 'ferramenta', 'ingrediente', 'material')),
            FOREIGN KEY (id_prestador) REFERENCES usuarios (id)
        )
        ''')

        # Tabela serviços
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            id_prestador INTEGER NOT NULL,
            FOREIGN KEY (id_prestador) REFERENCES usuarios (id)
        )
        ''')

        # Tabela agenda
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_servico INTEGER NOT NULL,
            data_hora_inicio TEXT NOT NULL,
            data_hora_fim TEXT NOT NULL,
            id_cliente INTEGER NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('pendente', 'concluido')),
            FOREIGN KEY (id_servico) REFERENCES servicos (id),
            FOREIGN KEY (id_cliente) REFERENCES usuarios (id)
        )
        ''')

        # Tabela pacotes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_prestador INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('produto', 'servico')),
            referencia INTEGER NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('pendente', 'em andamento', 'concluido')),
            FOREIGN KEY (id_cliente) REFERENCES usuarios (id),
            FOREIGN KEY (id_prestador) REFERENCES usuarios (id)
        )
        ''')

        # Tabela notificações
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        )
        ''')

        conexao.commit()
        conexao.close()
