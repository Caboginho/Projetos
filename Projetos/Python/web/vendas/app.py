from flask import Flask, render_template, redirect, url_for, request, session
from classes.banco import BancoDeDados
from classes.cliente import Cliente
from classes.prestador_servico import PrestadorServico
from routes.auth_routes import auth_blueprint
from routes.cliente_routes import cliente_blueprint
from routes.prestador_routes import prestador_blueprint

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
# Configura o banco
banco = BancoDeDados()

# Registra as Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(cliente_blueprint)
app.register_blueprint(prestador_blueprint)

@app.route('/')
def home():
    usuario = session.get('usuario')
    if not usuario:
        return render_template('base.html')  # Página inicial para não autenticados

    # Confirme que o usuário está no formato correto
    if isinstance(usuario, dict) and usuario.get('tipo') == 'prestador':
        return redirect(url_for('prestador.prestador_home'))
    elif isinstance(usuario, dict) and usuario.get('tipo') == 'cliente':
        return redirect(url_for('cliente.cliente_home'))
    else:
        return render_template('base.html', erro="Erro ao identificar o tipo de usuário.")

if __name__ == "__main__":
    BancoDeDados.inicializar_banco()
    print("Banco de dados inicializado com sucesso.")
    app.run(debug=True)
