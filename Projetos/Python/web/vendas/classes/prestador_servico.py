from .usuario import Usuario
class PrestadorServico(Usuario):
    def __init__(self, id, nome, email):
        super().__init__(id, nome, email, "prestador")

    def adicionar_produto(self, nome, preco, estoque, banco):
        try:
            banco.executar("INSERT INTO produtos (nome, preco, estoque, id_prestador) VALUES (?, ?, ?, ?)",
                           (nome, preco, estoque, self.id))
            return {"mensagem": "Produto adicionado com sucesso!"}
        except Exception as e:
            return {"erro": f"Erro ao adicionar produto: {str(e)}"}

    def adicionar_servico(self, nome, preco, banco):
        try:
            banco.executar("INSERT INTO servicos (nome, preco, id_prestador) VALUES (?, ?, ?)", (nome, preco, self.id))
            return {"mensagem": "Serviço adicionado com sucesso!"}
        except Exception as e:
            return {"erro": f"Erro ao adicionar serviço: {str(e)}"}

    def gerenciar_estoque(self, banco):
        try:
            produtos = banco.consultar("SELECT id, nome, estoque FROM produtos WHERE id_prestador = ?", (self.id,))
            return produtos
        except Exception as e:
            return {"erro": f"Erro ao consultar estoque: {str(e)}"}

    def gerenciar_agenda(self, banco):
        try:
            agenda = banco.consultar(
                "SELECT id, data_hora, id_cliente, status FROM agenda WHERE id_servico IN (SELECT id FROM servicos WHERE id_prestador = ?)", 
                (self.id,)
            )
            return agenda
        except Exception as e:
            return {"erro": f"Erro ao consultar agenda: {str(e)}"}

    def calcular_relevancia(self, banco):
        try:
            interacoes = banco.consultar("SELECT COUNT(*) FROM pacotes WHERE id_prestador = ?", (self.id,))
            relevancia = interacoes[0][0]
            banco.executar("UPDATE usuarios SET relevancia = ? WHERE id = ?", (relevancia, self.id))
            return {"mensagem": f"Relevância atualizada para: {relevancia}"}
        except Exception as e:
            return {"erro": f"Erro ao calcular relevância: {str(e)}"}

    