from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, id_cliente, nome, email):
        super().__init__(id_cliente, nome, email, "cliente")
        self.carrinho = []
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email

    def comprar(self, banco):
        for tipo, referencia in self.carrinho:
            if tipo == "produto":
                produto = banco.consultar("SELECT * FROM produtos WHERE id = ?", (referencia,))
                if produto:
                    estoque_atual = produto[0][3]
                    if estoque_atual > 0:
                        banco.executar("UPDATE produtos SET estoque = estoque - 1 WHERE id = ?", (referencia,))
                        banco.executar(
                            "INSERT INTO pacotes (id_cliente, id_prestador, tipo, referencia, status) VALUES (?, ?, ?, ?, 'pendente')",
                            (self.id, produto[0][4], tipo, referencia))
                        print(f"Produto comprado: {produto[0][1]}")
                    else:
                        print(f"Produto sem estoque: {produto[0][1]}")
            elif tipo == "servico":
                servico = banco.consultar("SELECT * FROM servicos WHERE id = ?", (referencia,))
                if servico:
                    banco.executar(
                        "INSERT INTO pacotes (id_cliente, id_prestador, tipo, referencia, status) VALUES (?, ?, ?, ?, 'pendente')",
                        (self.id, servico[0][3], tipo, referencia))
                    print(f"Serviço contratado: {servico[0][1]}")

        self.carrinho = []

    def acompanhar_servicos(self, banco):
        pacotes = banco.consultar("SELECT * FROM pacotes WHERE id_cliente = ?", (self.id,))
        for pacote in pacotes:
            print(f"Pacote ID: {pacote[0]}, Tipo: {pacote[3]}, Status: {pacote[5]}")
    
    def buscar_itens(self, banco, tipo, filtros=None):
        if tipo not in ["produtos", "servicos"]:
            print("Tipo inválido. Escolha entre 'produtos' ou 'servicos'.")
            return

        resultados = banco.buscar_produtos_servicos(tipo, filtros)
        if resultados:
            print(f"\n=== Resultados de {tipo.capitalize()} ===")
            for item in resultados:
                print(f"ID: {item[0]}, Nome: {item[1]}, Preço: {item[2]}")
        else:
            print("Nenhum item encontrado com os filtros fornecidos.")
            
    def adicionar_ao_carrinho(self, banco, item_id, quantidade):
        """
        Adiciona um item ao carrinho do cliente.
        """
        query = """
        INSERT INTO carrinho (id_cliente, id_item, quantidade)
        VALUES (%s, %s, %s)
        ON CONFLICT (id_cliente, id_item)
        DO UPDATE SET quantidade = carrinho.quantidade + EXCLUDED.quantidade;
        """
        banco.executar_query(query, (self.id_cliente, item_id, quantidade))

    def realizar_compra(self, banco):
        """
        Finaliza a compra para os itens no carrinho.
        """
        # Busca os itens do carrinho
        query_carrinho = "SELECT id_item, quantidade FROM carrinho WHERE id_cliente = %s"
        itens_carrinho = banco.buscar(query_carrinho, (self.id_cliente,))

        if not itens_carrinho:
            raise ValueError("O carrinho está vazio!")

        # Insere os itens no histórico de compras
        query_compra = """
        INSERT INTO pedidos (id_cliente, id_item, quantidade, data_compra)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
        """
        for item in itens_carrinho:
            banco.executar_query(query_compra, (self.id_cliente, item['id_item'], item['quantidade']))

        # Limpa o carrinho após a compra
        query_limpar_carrinho = "DELETE FROM carrinho WHERE id_cliente = %s"
        banco.executar_query(query_limpar_carrinho, (self.id_cliente,))

    def acompanhar_pedidos(self, banco):
        """
        Retorna o histórico de pedidos do cliente.
        """
        query = """
        SELECT p.id_pedido, p.data_compra, i.nome AS item, p.quantidade
        FROM pedidos p
        JOIN itens i ON p.id_item = i.id_item
        WHERE p.id_cliente = %s
        ORDER BY p.data_compra DESC;
        """
        return banco.buscar(query, (self.id_cliente,))
        
