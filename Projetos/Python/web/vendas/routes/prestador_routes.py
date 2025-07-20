from flask import Blueprint, request, jsonify
from classes.prestador_servico import PrestadorServico
from classes.banco import BancoDeDados
from flask import Blueprint, render_template, redirect, url_for, request,session

prestador_bp = Blueprint('prestador', __name__)
banco = BancoDeDados()

prestador_blueprint = Blueprint('prestador', __name__, url_prefix='/prestador')

@prestador_blueprint.route('/home')
def prestador_home():
    usuario = session.get('usuario')  # Recupera as informações do usuário
    prestador = PrestadorServico(usuario['id'],usuario['nome'],usuario['email'])
    if not usuario:
        return redirect(url_for('auth.login'))  # Redireciona para login se não estiver autenticado
    return render_template('prestador.html', usuario=prestador)

# Outras rotas para o prestador, se necessário
@prestador_blueprint.route('/adicionar_produto', methods=['POST','GET'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        estoque = request.form['estoque']
        id_prestador = session.get('usuario')['id']  # Verifica se o usuário está autenticado
        print(id_prestador)
        if not id_prestador:
            return {"erro": "Acesso negado"}, 403

        banco = BancoDeDados()
        try:
            banco.executar(
                '''
                INSERT INTO produtos (nome, preco, estoque, id_prestador,tipo)
                VALUES (?, ?, ?, ?,?)
                ''',
                (nome, preco, estoque, id_prestador, 'material')
            )
        except :
            print("Erro banco a escrever no banco de dados(Prestador Routes)")
            banco.fechar()
            return render_template('adicionar_produto.html')
        finally:
            banco.fechar()
        return redirect(url_for('prestador.meus_produtos'))

    return render_template('adicionar_produto.html')

@prestador_blueprint.route('/adicionar_servico', methods=['POST','GET'])
def adicionar_servico():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        id_prestador = session.get('usuario')['id']

        if not id_prestador:
            return {"erro": "Acesso negado"}, 403

        banco = BancoDeDados()
        banco.executar(
            '''
            INSERT INTO servicos (nome, preco, id_prestador)
            VALUES (?, ?, ?)
            ''',
            (nome, preco, id_prestador)
        )
        banco.fechar()
        return redirect(url_for('prestador.meus_servicos'))

    return render_template('adicionar_servico.html')

@prestador_blueprint.route('/estoque', methods=['GET'])
def estoque():
    estoque = []
    id_prestador = session.get('usuario')['id']
    if not id_prestador:
        return {"erro": "Acesso negado"}, 403

    banco = BancoDeDados()
    #produtos = banco.buscar_produtos_prestador(id_prestador)
    banco.fechar()
    return render_template('estoque.html',estoque = estoque)

@prestador_blueprint.route('/adicionar_agendamento', methods=['POST'])
def adicionar_agendamento():
    banco = BancoDeDados()
    id_servico = request.form['id_servico']
    data_hora_inicio = request.form['data_hora_inicio']
    data_hora_fim = request.form['data_hora_fim']
    id_cliente = session['usuario']['id']

    # Verificar conflitos
    conflito = banco.consultar(
        '''
        SELECT * FROM agenda
        WHERE
            (data_hora_inicio < ? AND data_hora_fim > ?)
            OR (data_hora_inicio < ? AND data_hora_fim > ?)
        ''',
        (data_hora_fim, data_hora_fim, data_hora_inicio, data_hora_inicio)
    )

    if conflito:
        banco.fechar()
        return "Conflito de horário! Escolha outro horário.", 409

    # Inserir agendamento
    banco.executar(
        '''
        INSERT INTO agenda (id_servico, data_hora_inicio, data_hora_fim, id_cliente, status)
        VALUES (?, ?, ?, ?, 'pendente')
        ''',
        (id_servico, data_hora_inicio, data_hora_fim, id_cliente)
    )
    # Enviar notificação ao cliente
    banco.enviar_notificacao(
    id_usuario=id_cliente,
    mensagem="Seu agendamento foi confirmado!"
)
    banco.fechar()
    
    return redirect(url_for('prestador.adicionar_agendamento'))

@prestador_blueprint.route('/meus_servicos', methods=['GET', 'POST'])
def meus_servicos():
    banco = BancoDeDados()
    id_prestador = session['usuario']['id']

    # Filtros
    nome_filtro = request.form.get('nome', None)

    query = '''
        SELECT id,nome, preco, id_prestador
        FROM servicos
        WHERE id_prestador = ?
    '''
    params = [id_prestador]

    servicos = banco.consultar(query, params)
    
    print(servicos)
    banco.fechar()
    return render_template('meus_servicos.html', servicos=servicos)

@prestador_blueprint.route('/meus_produtos', methods=['GET', 'POST'])
def meus_produtos():
    banco = BancoDeDados()
    id_prestador = session['usuario']['id']

    # Filtros
    tipo_filtro = request.form.get('tipo', None)
    nome_filtro = request.form.get('nome', None)

    query = '''
        SELECT nome, preco, estoque, tipo
        FROM produtos
        WHERE id_prestador = ?
    '''
    params = [id_prestador]

    if tipo_filtro:
        query += ' AND tipo = ?'
        params.append(tipo_filtro)

    if nome_filtro:
        query += ' AND nome LIKE ?'
        params.append(f"%{nome_filtro}%")

    produtos = banco.consultar(query, params)
    banco.fechar()
    return render_template('meus_produtos.html', produtos=produtos)

# Rota para logout do cliente
@prestador_blueprint.route('/logout')
def logout():
    session.pop("usuario", None)  # Remove o usuário da sessão
    return redirect(url_for('auth.login'))

@prestador_blueprint.route('/agenda')
def agenda():
    agenda = []
    id_prestador = session.get('usuario')['id']
    if not id_prestador:
        return {"erro": "Acesso negado"}, 403

    banco = BancoDeDados()
    #agendas = banco.buscar_agendas(id_prestador)
    banco.fechar()
    return render_template('agenda.html', agenda = agenda)