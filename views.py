from flask import render_template, request, redirect, session, flash, url_for, Blueprint
from app import db
from models import Jogos, Usuarios

view = Blueprint('view', __name__)

@view.route('/')
def index():
    
    print('rodando')
    lista = Jogos.query.order_by(Jogos.id)
    
    # devido à padronização do flask de utilizar a pasta 'templates', ele já busca o html nela por
    # padrão, sendo assim, somente o nome do arquivo precisa ser passado
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@view.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@view.route('/criar', methods=['POST'])
def criar():
    # O flask identifica o dado que deve ser captado pelo que foi recebido no form pela tag pelo 
    # parâmetro identificador "name" na tag do HTML
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome = nome).first()
    
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()
    
    # 'index' é a função que instancia a página da rota '/'
    return redirect(url_for('index'))

@view.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@view.route('/autenticar', methods=['POST'])
def autenticar():
    
    usuario = Usuarios.query.filter_by(nickname = request.form['usuario']).first()
    
    # session é um recurso do python que permite persistirmos dados por mais de uma requisição, 
    # salvando-os nos cookies do navegador.
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))
    
@view.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))