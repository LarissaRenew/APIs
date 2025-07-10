from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API da Ellevo está no ar!"

@app.route("/abrir-chamado", methods=["POST"])
def abrir_chamado():
    # Apenas simulação de resposta da API Ellevo
    dados_recebidos = request.get_json()
    return jsonify({
        "mensagem": "Chamado recebido com sucesso!",
        "dados_recebidos": dados_recebidos
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # para Render
    app.run(host="0.0.0.0", port=port)
