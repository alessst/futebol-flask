from flask import Flask, render_template, request
import csv
import random


app = Flask(__name__)
times_data = []
jdata = []

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
    return render_template("tabela.html", escudo=escudo, nome_time=nome_time)



if __name__ == "__main__":
    app.run(debug=True)
