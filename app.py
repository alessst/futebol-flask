from flask import Flask, render_template, request
import urllib.request, json
import random

url = 'https://api.api-futebol.com.br/v1/campeonatos/14/tabela'
headers = {'Authorization': 'Bearer test_af647478dcd44baa8bc59073498bf7'}

app = Flask(__name__)
def obter_dados_time(n):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    jdata = json.loads(data)
    dados_time = jdata[n]
    time = dados_time["time"]
    nome = time["nome_popular"]
    escudo_time = time["escudo"]
    return nome, escudo_time

@app.route("/", methods=['GET', 'POST'])
def tabela():
    numero = random.randint(0, 19)
    if request.method == 'POST':
        valor = request.form.get('valor')
       

    nome_time, escudo = obter_dados_time(numero)
    print(nome_time)
    return render_template("tabela.html", escudo=escudo, nome_time=nome_time)



if __name__ == "__main__":
    app.run(debug=True)
