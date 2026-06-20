from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def inicio():
    return '''
    <!doctype html>
    <html>
    <head><title>Teste da API</title></head>
    <body style="font-family:sans-serif; max-width:400px; margin:50px auto;">
        <h2>Simulador de Compra</h2>
        <input id="nome" placeholder="Seu nome" style="width:100%;padding:8px;margin:5px 0;"><br>
        <input id="email" placeholder="Seu email" style="width:100%;padding:8px;margin:5px 0;"><br>
        <button onclick="comprar()" style="padding:10px 20px;">Comprar</button>
        <pre id="resposta" style="background:#f0f0f0;padding:10px;margin-top:20px;"></pre>
        <script>
        async function comprar(){
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const r = await fetch('/compra', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({nome, email})
            });
            const data = await r.json();
            document.getElementById('resposta').innerText = JSON.stringify(data, null, 2);
        }
        </script>
    </body>
    </html>
    '''

@app.route('/compra', methods=['POST'])
def compra():
    dados = request.get_json()
    nome = dados.get('nome', 'cliente')
    email = dados.get('email')
    if not email:
        return jsonify({"status": "erro", "mensagem": "email é obrigatório"}), 400
    print(f"[SIMULAÇÃO] Enviando e-mail para {email}")
    return jsonify({"status": "ok", "mensagem": f"Olá {nome}, confirmação enviada para {email}"})

app.run(host='0.0.0.0', port=8080)
