from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SUAS CHAVES OneSignal
APP_ID = "3cc0fb0d-546a-49c3-bae9-fbe6ce9bfcfe"
API_KEY = "os_v2_app_htapwdkunje4hoxj7ptm5g747yq2lq254ikutpfvbascgpcavaonmdjk6yq2lq254ikutpfvbascgpcavaonmdjk6y4o5mhf45b2dca447ij6ocfejcujm5v5ndd275rwgf5rqq"

# Dicionário: username → Player ID
usuarios = {}

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    username = data.get('username', '').lower()
    player_id = data.get('player_id', '')
    
    if not username or not player_id:
        return jsonify({"erro": "Faltou username ou player_id"}), 400
    
    usuarios[username] = player_id
    return jsonify({
        "status": "ok", 
        "msg": f"✅ @{username} registrado!",
        "usuarios": list(usuarios.keys())
    })

@app.route('/usuarios')
def listar_usuarios():
    return jsonify({"usuarios": list(usuarios.keys())})

@app.route('/enviar/<username>/<mensagem>')
def enviar(username, mensagem):
    username = username.lower()
    
    if username not in usuarios:
        return f"❌ Usuário @{username} não encontrado. Cadastre primeiro!"
    
    player_id = usuarios[username]
    
    # SIMULAÇÃO (sem erro UUID) - mude SIMULAR=False pra OneSignal real
    SIMULAR = True  # ← Mude pra False quando tiver Player ID real
    
    if SIMULAR:
        return f"✅ SIMULAÇÃO OK: '{mensagem}' seria enviada pra @{username} (Player ID: {player_id})"
    
    # OneSignal real (só ativa com SIMULAR=False)
    url = "https://onesignal.com/api/v1/notifications"
    headers = {"Content-Type": "application/json", "Authorization": f"Basic {API_KEY}"}
    payload = {
        "app_id": APP_ID,
        "include_player_ids": [player_id],
        "contents": {"pt": mensagem},
        "headings": {"pt": f"Nova msg pra @{username}"}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return f"✅ OneSignal: {response.status_code} - {response.text}"

@app.route('/')
def home():
    return f"""
    <h1>🚀 Backend Zap Mensagens ✅</h1>
    <p><b>Testes:</b></p>
    <ul>
        <li><a href="/usuarios">/usuarios</a> → lista cadastrados</li>
        <li>POST /registrar → {{"username": "joao", "player_id": "abc123"}}</li>
        <li><a href="/enviar/joao123/Teste">/enviar/joao/Ola</a></li>
    </ul>
    <p><b>Status:</b> {len(usuarios)} usuários cadastrados</p>
    """

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
