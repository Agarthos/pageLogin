from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Conexão com banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestao_alunos"
)

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    if not nome or not email or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    cursor = db.cursor()
    query = "INSERT INTO alunos (nome, email, senha, curso_id, data_matricula) VALUES (%s, %s, %s, %s, NOW())"
    cursor.execute(query, (nome, email, senha, 1))
    db.commit()
    return jsonify({"mensagem": "Aluno cadastrado com sucesso!"})

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE email=%s AND senha=%s", (email, senha))
    aluno = cursor.fetchone()

    if aluno:
        return jsonify({"sucesso": True, "mensagem": "Login correto!"})
    else:
        return jsonify({"sucesso": False, "mensagem": "Email ou senha incorretos."}), 401

if __name__ == '__main__':
    app.run(debug=True)
