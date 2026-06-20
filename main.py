from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def inicio():
    return "API funcionando. Use POST em /compra"

@app.route('/compra', methods=['POST'])
def compra():
    dados = request.get_json()
    nome = dados.get('nome', 'cliente')
    email = dados.get('email')
    
    print(f"[SIMULAÇÃO] Enviando e-mail para {email}")
    
    return jsonify({
        "status": "ok",
        "mensagem": f"Olá {nome}, confirmação enviada para {email}"
    })

app.run(host='0.0.0.0', port=8080)