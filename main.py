import os
from flask import Flask, request, jsonify
import resend

app = Flask(__name__)
resend.api_key = os.getenv("RESEND_API_KEY")

@app.route('/')
def inicio():
    return '''<!doctype html><html><head><title>Simulador</title></head>
<body style="font-family:sans-serif;max-width:400px;margin:50px auto;">
<h2>Simulador de Compra</h2>
<input id="nome" placeholder="Seu nome" style="width:100%;padding:8px;margin:5px 0;"><br>
<input id="email" placeholder="Seu email" style="width:100%;padding:8px;margin:5px 0;"><br>
<button onclick="comprar()" style="padding:10px 20px;">Comprar</button>
<pre id="resposta" style="background:#f0f0f0;padding:10px;margin-top:20px;"></pre>
<script>
async function comprar(){
  const nome=document.getElementById('nome').value;
  const email=document.getElementById('email').value;
  const r=await fetch('/compra',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,email})});
  document.getElementById('resposta').innerText=JSON.stringify(await r.json(),null,2);
}
</script></body></html>'''

@app.route('/compra', methods=['POST'])
def compra():
    dados = request.get_json() or {}
    nome = dados.get('nome','cliente')
    email = dados.get('email')
    
    if not email:
        return jsonify({"status":"erro","mensagem":"email obrigatório"}),400
    
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": f"Confirmação - {nome}",
            "html": f"<h1>Olá {nome}!</h1><p>Sua compra foi confirmada. Este é seu primeiro email real do SaaS.</p>"
        })
        return jsonify({"status":"ok","mensagem":f"Email enviado para {email}"})
    except Exception as e:
        return jsonify({"status":"erro","detalhe":str(e)}),500

app.run(host='0.0.0.0', port=8080)