from flask import Blueprint, render_template, redirect, url_for, request, session
from classes.cliente import Cliente
from classes.banco import BancoDeDados

# Blueprint para rotas relacionadas ao cliente
cliente_blueprint = Blueprint('cliente', __name__, url_prefix='/cliente')

# Rota para a página inicial do cliente
@cliente_blueprint.route('/home')
def cliente_home():
    usuario = session.get("usuario")  # Recupera as informações do usuário
    if not usuario:
        return redirect(url_for('auth.login'))  # Redireciona para login se não estiver autenticado
    
    cliente = Cliente(usuario['id'], usuario['nome'], usuario['email'])  # Instancia um objeto Cliente
    return render_template('cliente.html', usuario=cliente)

# Rota para adicionar itens ao carrinho
@cliente_blueprint.route('/add_carrinho', methods=['POST'])
def add_carrinho():
    item_id = request.form.get("item_id")  # Obtém o ID do item do formulário
    quantidade = request.form.get("quantidade", 1)  # Quantidade padrão é 1 se não fornecida
    
    # Lógica para adicionar ao carrinho
    banco = BancoDeDados()
    usuario = session.get("usuario")
    if usuario:
        cliente = Cliente(usuario['id'], usuario['nome'], usuario['email'])
        cliente.adicionar_ao_carrinho(banco, item_id, quantidade)  # Método hipotético na classe Cliente
    
    return redirect(url_for('cliente.cliente_home'))

# Rota para processar uma compra
@cliente_blueprint.route('/comprar', methods=['POST'])
def comprar():
    usuario = session.get("usuario")
    if usuario:
        banco = BancoDeDados()
        cliente = Cliente(usuario['id'], usuario['nome'], usuario['email'])
        cliente.realizar_compra(banco)  # Método para finalizar a compra
    
    return redirect(url_for('cliente.cliente_home'))

# Rota para acompanhar pedidos
@cliente_blueprint.route('/acompanhar')
def acompanhar():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for('auth.login'))
    
    banco = BancoDeDados()
    cliente = Cliente(usuario['id'], usuario['nome'], usuario['email'])
    pedidos = cliente.acompanhar_pedidos(banco)  # Método para buscar pedidos
    
    return render_template('acompanhar.html', pedidos=pedidos)

# Rota para buscar produtos ou serviços
@cliente_blueprint.route('/buscar', methods=['GET', 'POST'])
def buscar():
    banco = BancoDeDados()
    id_cliente = session['usuario']['id']

    # Filtros
    nome_filtro = request.form.get('nome', None)

    query = '''
        SELECT nome, preco, tipo
        FROM servicos
        WHERE id_prestador = ?
    '''
    params = [id_cliente]

    servicos = banco.consultar(query, params)
    query = '''
        SELECT nome, preco,id_prestador
        FROM produtos
        WHERE id_prestador = ?
    '''
    produtos = banco.consultar(query, params)
    resultados = produtos + servicos   
    return render_template('buscar.html', resultados=resultados)

# Rota para logout do cliente
@cliente_blueprint.route('/logout')
def logout():
    session.pop("usuario", None)  # Remove o usuário da sessão
    return redirect(url_for('auth.login'))
