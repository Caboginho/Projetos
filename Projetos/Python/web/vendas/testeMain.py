import random
from classes.banco import BancoDeDados, inicializar_banco
from classes.cliente import Cliente
from classes.prestador_servico import PrestadorServico

def criar_usuarios(banco, quantidade):
    """Cria clientes e prestadores aleatoriamente."""
    for i in range(quantidade):
        tipo = "cliente" if i % 2 == 0 else "prestador"
        nome = f"Usuario_{tipo}_{i}"
        email = f"{nome.lower()}@teste.com"
        senha = "123456"
        banco.executar("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)", (nome, email, senha, tipo))

def criar_produtos_servicos(banco, quantidade):
    """Cria produtos e serviços para prestadores aleatórios."""
    prestadores = banco.consultar("SELECT id FROM usuarios WHERE tipo = 'prestador'")
    for _ in range(quantidade):
        prestador_id = random.choice(prestadores)[0]
        if random.choice([True, False]):
            nome = f"Produto_{random.randint(1, 1000)}"
            preco = round(random.uniform(10, 500), 2)
            estoque = random.randint(1, 100)
            banco.executar("INSERT INTO produtos (nome, preco, estoque, id_prestador) VALUES (?, ?, ?, ?)",
                           (nome, preco, estoque, prestador_id))
        else:
            nome = f"Servico_{random.randint(1, 1000)}"
            preco = round(random.uniform(50, 1000), 2)
            banco.executar("INSERT INTO servicos (nome, preco, id_prestador) VALUES (?, ?, ?)",
                           (nome, preco, prestador_id))

def criar_transacoes(banco, quantidade):
    """Gera transações entre clientes e produtos/serviços."""
    clientes = banco.consultar("SELECT id FROM usuarios WHERE tipo = 'cliente'")
    produtos = banco.consultar("SELECT id, id_prestador FROM produtos")
    servicos = banco.consultar("SELECT id, id_prestador FROM servicos")

    for _ in range(quantidade):
        cliente_id = random.choice(clientes)[0]
        if random.choice([True, False]) and produtos:
            produto = random.choice(produtos)
            produto_id, prestador_id = produto
            banco.executar(
                "INSERT INTO pacotes (id_cliente, id_prestador, tipo, referencia, status) VALUES (?, ?, 'produto', ?, 'pendente')",
                (cliente_id, prestador_id, produto_id))
            banco.executar("UPDATE produtos SET estoque = estoque - 1 WHERE id = ? AND estoque > 0", (produto_id,))
        elif servicos:
            servico = random.choice(servicos)
            servico_id, prestador_id = servico
            banco.executar(
                "INSERT INTO pacotes (id_cliente, id_prestador, tipo, referencia, status) VALUES (?, ?, 'servico', ?, 'pendente')",
                (cliente_id, prestador_id, servico_id))
            data_hora = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} {random.randint(8, 18):02d}:00:00"
            banco.executar(
                "INSERT INTO agenda (id_servico, data_hora, id_cliente, status) VALUES (?, ?, ?, 'pendente')",
                (servico_id, data_hora, cliente_id))

def main():
    inicializar_banco()
    banco = BancoDeDados()

    print("Criando usuários...")
    criar_usuarios(banco, quantidade=100)  # 50 clientes e 50 prestadores

    print("Criando produtos e serviços...")
    criar_produtos_servicos(banco, quantidade=500)  # 500 produtos/serviços aleatórios

    print("Criando transações...")
    criar_transacoes(banco, quantidade=1000)  # 1000 transações aleatórias

    print("Teste concluído!")
    banco.fechar()

if __name__ == "__main__":
    main()
