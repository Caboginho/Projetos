from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from classes.banco import BancoDeDados

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
@auth_blueprint.route('/home')
def home():
    return render_template('base.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        banco = BancoDeDados()
        usuario = banco.consultar(
            "SELECT id, nome, email, tipo FROM usuarios WHERE email = ? AND senha = ?", 
            (email, senha)
        )

        if usuario:
            session['usuario'] = {
                'id': usuario[0][0],
                'nome': usuario[0][1],
                'email': usuario[0][2],
                'tipo': usuario[0][3]
            }
            if session['usuario']['tipo'] == 'prestador':
                return redirect(url_for('prestador.prestador_home'))
            return redirect(url_for('cliente.cliente_home'))
        else:
            return render_template('login.html', erro="Usuário ou senha inválidos.")
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Coleta os dados de registro do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = 'cliente'
        
        # Lógica de cadastro no banco
        banco = BancoDeDados()
        try:
            banco.executar("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)", 
                           (nome, email, senha, perfil))  # 'cliente' como exemplo
            return redirect(url_for('auth.login'))  # Após registro, redireciona para login
        except Exception as e:
            return render_template('cadastro.html', erro="Erro ao cadastrar usuário.")
    
    return render_template('cadastro.html')

@auth_blueprint.route('/mudar_perfil', methods=['POST', 'GET'])
def mudar_perfil():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    
    novo_tipo = 'prestador' if usuario['tipo'] == 'cliente' else 'cliente'
    
    banco = BancoDeDados()
    banco.executar("UPDATE usuarios SET tipo = ? WHERE id = ?", (novo_tipo, usuario['id']))
    
    # Atualiza o tipo na sessão
    session['usuario']['tipo'] = novo_tipo

    # Redireciona para a página correspondente
    if novo_tipo == 'prestador':
        return redirect(url_for('prestador.prestador_home'))
    return redirect(url_for('cliente.cliente_home'))

@auth_blueprint.route('/logout')
def logout():
    session.clear()  # Limpa os dados da sessão
    return redirect(url_for('auth.login'))  # Redireciona para a página de login

@auth_blueprint.route('/notificacoes', methods=['GET'])
def listar_notificacoes():
    banco = BancoDeDados()
    id_usuario = session['usuario']['id']

    notificacoes = banco.consultar(
        '''
        SELECT mensagem, lida, data_criacao
        FROM notificacoes
        WHERE id_usuario = ?
        ORDER BY data_criacao DESC
        ''',
        (id_usuario,)
    )
    banco.fechar()
    return render_template('notificacoes.html', notificacoes=notificacoes)
