from flask import Flask, render_template
from select import select
from models import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/lista_salgado')
# def lista_salgado():
#     sql_salgados = select(Salgado)