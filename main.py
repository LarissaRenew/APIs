from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API da Ellevo está no ar!"

@app.route("/abrir-chamado", methods=["POST"])
def abrir_chamado():
    return jsonify({"mensagem": "A rota está funcionando!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # para Render
    app.run(host="0.0.0.0", port=port)
