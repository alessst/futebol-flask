from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pontuacao.sqlite3'
db = SQLAlchemy(app)

class Pontuacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    pt = db.Column(db.String(10))

    def __init__(self, nome, pt):
        self.nome = nome
        self.pt = pt

with open('times.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    jdata = list(reader)

def obter_dados_time(n):
    dados_time = jdata[n]
    nome = dados_time["nome_popular"]
    escudo_time = dados_time["escudo"]
    return nome, escudo_time

@app.route("/obter_nova_imagem")
def obter_nova_imagem():
    numero = random.randint(0, 122)
    nome, escudo = obter_dados_time(numero)
    return jsonify({"nome": nome, "escudo": escudo})

@app.route("/", methods=['GET', 'POST'])
def tabela():
    numero = random.randint(0, 122)
    nome_time, escudo = obter_dados_time(numero)

    if request.method == "POST":
        nome = request.form.get("nome_str")
        ponto = request.form.get("ponto_str")
        print(f"nome:{nome} ||||| pontos: {ponto}")
        if nome == None or ponto == None:
            return render_template("tabela.html", escudo=escudo, nome_time=nome_time, jogadores=Pontuacao.query.all())
        else:
            print(f"nome:{nome} ||||| pontos: {ponto}")
            jogador = Pontuacao(nome, ponto)
            db.session.add(jogador)
            db.session.commit()
    
    return render_template("tabela.html", escudo=escudo, nome_time=nome_time, jogadores=Pontuacao.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
