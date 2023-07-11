from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv
import random


lista_pontos = []
app = Flask(__name__)
jdata = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pontuacao.sqlite3'

db = SQLAlchemy(app)

class pontos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50))
	pt = db.Column(db.String(10))

	def __init__(self, nome, pt):
		self.nome = nome
		self.pt = pt
                
with open('times.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        jdata.append(row)

def obter_dados_time(n):
    dados_time = jdata[n]
    nome = dados_time["nome_popular"]
    escudo_time = dados_time["escudo"]
    return nome, escudo_time

@app.route("/", methods=['GET', 'POST'])
def tabela():
    numero = random.randint(0, 39)
    nome_time, escudo = obter_dados_time(numero)
    print(nome_time)
    return render_template("tabela.html", escudo=escudo, nome_time=nome_time, pontos=pontos.query.all())

@app.route("/add_pontos", methods=['GET', 'POST'])
def jogador():
    nome = request.form.get("nome")
    ponto = request.form.get("ponto")
    if request.method == "POST":
        jogador = pontos(nome, ponto)
        db.session.add(jogador)
        db.session.commit()
        return redirect(url_for("tabela"))
    return render_template("jogador.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
