from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///device.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

from Sandymodel import *

@app.route('/')
def index():
	return "Junior pega Homem!"


@app.route('/exibe', methods=['GET'])
def exibeTudo():
	dados = []
	for i in Device.query.all():
		print i.name, i.valor.temp, i.valor.umidade, i.valor.date
		dados.append({'id': i.id, 'Nome': i.name, 'Temperatura': i.valor.temp, 'Umidade': i.valor.umidade, 'Data': i.valor.date.isoformat()})

	return json.dumps(dados)


@app.route('/inserir', methods=['POST'])
def inserirDado():
	if not request.json:
		return jsonify({'status': False})

	p = request.get_json()
	j = Device()
	j.name = p['name']
	j.valor.temp = p['temp']
	j.valor.umidade = p['umidade']
	j.valor.date = datetime.datetime.now()
	db.session.add(j)
	db.session.commit()

	return jsonify({'status:': True})


if __name__ == '__main__':
	app.run(debug=True)
