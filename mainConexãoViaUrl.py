from flask import Flask, request, jsonify
import pandas as pd
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API da Ellevo está no ar!"

@app.route("/abrir-chamado", methods=["POST"])
def abrir_chamado():
    try:
        data = request.get_json()
        excel_url = data.get("excel_url")

        if not excel_url:
            return jsonify({"erro": "Parâmetro 'excel_url' é obrigatório"}), 400

        # 🧪 Testar download
        response = requests.get(excel_url)
        if response.status_code != 200:
            return jsonify({"erro": f"Falha ao baixar o Excel: {response.status_code}"}), 500

        # 🧪 Testar leitura
        try:
            df = pd.read_excel(BytesIO(response.content))
        except Exception as e:
            return jsonify({"erro": f"Erro ao ler planilha: {str(e)}"}), 500

        return jsonify({"linhas": df.head().to_dict()}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

