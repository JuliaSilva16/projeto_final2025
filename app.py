from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes import *  # Importa as funções de comunicação com a API
from functools import wraps

app = Flask(__name__)
# A SECRET_KEY é essencial para gerenciar a sessão (session)
app.config['SECRET_KEY'] = 'supersecretkey'  # Use uma chave segura


# --- Rotas de Login/Cadastro/Home/Logout ---

@app.route('/', methods=['GET'])
def inicial():
    # Se já estiver logado, redireciona para a Home
    if 'access_token' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
def home():
    # A variável 'username' será usada no template home.html
    username = session.get('user_nome', 'Usuário')
    return render_template('home.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_response = {
            'email': request.form.get('email'),
            'senha': request.form.get('senha')
        }
        post = post_login(login_response)

        if isinstance(post, dict) and "error" in post:
            flash("Erro ao logar: " + post['error'], "danger")
        else:
            token = post.get('access_token')
            papel = post.get('papel')
            nome = post.get('nome')  # Supondo que a API retorna o nome

            if token:
                session['access_token'] = token
                session['user_papel'] = papel  # Guardar o papel
                session['user_nome'] = nome  # Guardar o nome para exibição
                flash("Logado com sucesso!", "success")
                return redirect(url_for('home'))
            else:
                flash("Erro desconhecido ao logar.", 'danger')

    if 'access_token' in session:
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    """Remove o token, papel e nome da sessão e redireciona para o login."""
    session.pop('access_token', None)
    session.pop('user_papel', None)
    session.pop('user_nome', None)
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for('login'))


@app.route('/usuario/cadastro', methods=['GET', 'POST'])
def usuario_cadastro():
    if request.method == 'POST':
        user_response = {
            'nome': request.form.get('nome'),
            'email': request.form.get('email'),
            'senha': request.form.get('senha'),
            'papel': request.form.get('papel'),
        }
        post = post_cadastro(user_response)

        if isinstance(post, dict) and "error" in post:
            flash(f"Erro no cadastro: {post['error']}", "danger")
        else:
            flash("Cadastro realizado com sucesso", "success")
            return redirect(url_for('login'))

    return render_template('cadastro_funcionario.html')


# --- Rotas de Dados ---

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    # Verifica se o usuário é funcionário
    if session.get('user_papel') != 'funcionario':
        flash("Acesso restrito a funcionários.", "danger")
        return redirect(url_for('home'))

    data = get_usuarios()

    if 'error' in data:
        flash(data['error'], 'danger')
        alunos = []
    else:
        # A API retorna a chave 'usuarios'
        alunos = data.get('usuarios', [])

    return render_template("funcionarios.html", alunos=alunos)


@app.route('/alimento/novo_alimento', methods=['GET', 'POST'])
def alimento_novo():
    token = session.get('access_token')

    if session.get('user_papel') != 'funcionario':
        flash("Acesso restrito a funcionários.", "danger")
        return redirect(url_for('home'))

    if not token:
        flash("Você precisa estar logado para cadastrar alimentos.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        alimento_response = {
            'nome': request.form.get('nome'),
            'valor': request.form.get('valor'),
            'quantidade': request.form.get('quantidade'),
            'descricao': request.form.get('descricao'),
            'marca': request.form.get('marca'),
            'categoria': request.form.get('categoria'),
        }

        post_ali = post_alimento(alimento_response, token)

        if isinstance(post_ali, dict) and "error" in post_ali:
            flash(f"Erro no cadastro: {post_ali['error']}", "danger")
        else:
            flash("Cadastro realizado com sucesso", "success")
            return redirect(url_for('listar_alimento'))

    return render_template('cadastro_alimentos.html')


@app.route('/alimento', methods=['GET'])
def listar_alimento():
    data = get_alimento()

    if 'error' in data:
        flash(data['error'], 'danger')
        alimento = []
    else:
        alimento = data.get('alimento', [])

    return render_template("alimentos.html", alimento=alimento)


if __name__ == '__main__':
    print("Iniciando o Front-end...")
    # Alterando a porta padrão para 5000 para evitar conflito com a API em 5001
    app.run(debug=True, port=5000)
