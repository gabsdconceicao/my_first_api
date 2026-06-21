import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
import resend

app = Flask(__name__)
resend.api_key = os.getenv("RESEND_API_KEY")

# --- BANCO ---
def init_db():
    conn = sqlite3.connect('compras.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        data TEXT,
        resend_id TEXT
    )''')
    conn.close()

init_db()

@app.route('/')
def inicio():
    return '''<!doctype html><html><head><title>Simulador</title></head>
<body style="font-family:sans-serif;max-width:400px;margin:50px auto;">
<h2>Simulador de Compra</h2>
<input id="nome" placeholder="Seu nome" style="width:100%;padding:8px;margin:5px 0;"><br>
<input id="email" placeholder="Seu email" style="width:100%;padding:8px;margin:5px 0;"><br>
<button onclick="comprar()" style="padding:10px 20px;">Comprar</button>
<pre id="resposta" style="background:#f0f0f0;padding:10px;margin-top:20px;"></pre>
<p><a href="/admin" target="_blank">Ver vendas (/admin)</a></p>
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
        # 1. envia email
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": f"Confirmação - {nome}",
            "html": f"<h1>Olá {nome}!</h1><p>Sua compra foi confirmada.</p>"
        })
        resend_id = r.get('id')

        # 2. salva no banco
        conn = sqlite3.connect('compras.db')
        conn.execute("INSERT INTO compras (nome,email,data,resend_id) VALUES (?,?,?,?)",
                     (nome, email, datetime.now().isoformat(), resend_id))
        conn.commit()
        conn.close()

        return jsonify({"status":"ok","mensagem":f"Email enviado e venda salva para {email}"})
    except Exception as e:
        return jsonify({"status":"erro","detalhe":str(e)}),500

@app.route('/admin')
def admin():
    conn = sqlite3.connect('compras.db')
    rows = conn.execute("SELECT id, nome, email, data FROM compras ORDER BY id DESC").fetchall()
    conn.close()
    
    html = "<h2>Histórico de Vendas</h2><table border=1 cellpadding=5><tr><th>ID</th><th>Nome</th><th>Email</th><th>Data</th></tr>"
    for id_, nome, email, data in rows:
        html += f"<tr><td>{id_}</td><td>{nome}</td><td>{email}</td><td>{data[:19]}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)