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

        df = pd.read_excel(excel_url)

        chamados = []
        token = os.environ.get("TOKEN_ELLEVO")  # Token seguro via variável de ambiente

        for _, row in df.iterrows():
            prazo_str = ""
            try:
                prazo_str = pd.to_datetime(row["prazo"]).isoformat()
            except:
                pass  # Se der erro, deixa em branco

            payload = {
                "title": row["titulo"],
                "private": 1,
                "generatorReferenceCode": row["solicitante"],
                "customerReferenceCode": row["cliente"],
                "requesterReferenceCode": row["solicitante"],
                "serviceReferenceCode": row["servico"],
                "responsibleReferenceCode": row["responsavel"],
                "status": "concluded",
                "dueDate": prazo_str,
                "forms": [
                    {
                        "referenceCode": row["formulario"],
                        "fieldsValues": {
                            "ENTRADADETEXTO-638862167990": row["campo_texto"],
                            "NUMEROENTERO-638862298298": str(row["campo_numero"])
                        }
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            response = requests.post("https://renewsolutions.ellevo.com/api/v1/ticket", json=payload, headers=headers)

            chamados.append({
                "linha": row.to_dict(),
                "status_code": response.status_code,
                "resposta": response.json() if response.status_code in [200, 201] else response.text
            })

        return jsonify({"resultado": chamados}), 200

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"erro": str(e)}), 500
