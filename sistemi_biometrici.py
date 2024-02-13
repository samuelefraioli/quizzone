from flask import Flask, render_template, request, redirect
import random
import json

app = Flask(__name__)

@app.route('/')
def index():

    with open('domande.json','r') as file:
        domande = json.load(file)

    # Se il totale di domande è zero, visualizza un messaggio
    if domande['totali'] == 0:
        return "Non ci sono domande nel database."

    if len(domande['fatte']) == domande['totali']:
        return "Hai risposto correttamente a tutte le domande. <a href='http://localhost:999/reset'>Ricomincia</a>"

    # Genera un numero casuale e verifica se esiste nella tabella 'fatte'
    numero_domanda = random.randint(1, domande['totali'])

    while True:
        if numero_domanda in domande['fatte']:
            numero_domanda = random.randint(1, domande['totali'])
        else:
            testo = domande[str(numero_domanda)]['domanda']
            risposte = domande[str(numero_domanda)]['risposte']
            return render_template('domanda.html', testo=testo, risposte=risposte, domanda=numero_domanda)

@app.route('/submit', methods=['POST'])
def submit():
    with open('domande.json','r') as file:
        domande = json.load(file)
    risposta = request.form.get('risposta')
    domanda = request.form.get('domanda')
    if domande[domanda]['giusta']==risposta:
        domande['fatte'].append(int(domanda))
        with open('domande.json', 'w') as file:
            json.dump(domande, file, indent=4)
        return "Giusto <a href='http://localhost:999'>Continua</a>"
    else:
        return "Sbagliato <a href='http://localhost:999'>Continua</a>"

@app.route('/reset', methods=['GET'])
def reset():
    with open('domande.json', 'r') as file:
        domande = json.load(file)
        domande['fatte'] = []
    with open('domande.json', 'w') as newfile:
        json.dump(domande, newfile, indent=4)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=999, debug=True)
