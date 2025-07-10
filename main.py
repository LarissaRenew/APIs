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

        for _, row in df.iterrows():
            payload = {
                "title": row["titulo"],
                "private": 1,
                "generatorReferenceCode": row["solicitante"],
                "customerReferenceCode": row["cliente"],
                "requesterReferenceCode": row["solicitante"],
                "serviceReferenceCode": row["servico"],
                "responsibleReferenceCode": row["responsavel"],
                "status": "concluded",
                "dueDate": row["prazo"],
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
                "Authorization": "Bearer "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyOTI4NTQ5ODFDNDM4NjBEQkMwREE1OUNCMENDNzk1Mzg3RUNDNDMiLCJ0eXAiOiJKV1QifQ.eyJlbGxldm8vbGFuZ3VhZ2UiOiJwdC1CUiIsImVsbGV2by90ZW5hbnQvaWQiOiI2Mjg1M2UwMDAyNjE5ZjgzMjM1MzYzZWQiLCJlbGxldm8vc3ViLWRvbWFpbiI6InJlbmV3c29sdXRpb25zIiwiZWxsZXZvL3RpbWUtem9uZS1vZmZzZXQiOiItMTgwIiwiZWxsZXZvL2NyZWF0ZWQtYXQiOiI2LzIzLzIwMjUgNTozNzo0NiBQTSIsImlzcyI6IkVsbGV2byIsImF1ZCI6InJlbmV3c29sdXRpb25zIn0.fnuE_UD1ZdmASklBuVrKggDQQyQnmEB_Tp6UsSR7hBeo8bgnQ3FpkFev613zhI0VdRU9EPL6xUCC72BTzi4G2IrTFtN7n8XFSFki6MFE9g9WjjIA6uy6qK3sZmPvgR7nnURrumH0Kd6xZbJJ50aAyrpgans0qEdblXbyWznvKuTBeLjxgZFY2qylJlh0LSmcqnBty-SjxyPNSvCX0lQOqDk3PcRRac6XOR5rLom4aPWugAdRzeoDPuuI7AY-d9InKFoVrFgcfG9X3fkkwh1zsKCdVKJZ2g3cGkhPY3PagHYbfzoTKw7-nHFfOdfvfA18Z8LfBdCTvPYWhXn8Jt7xnPSH_UPdUyd6SV27kqeDaoH88Q1PdDNM-YskzMnZqDKy5vAfdCosYa3UaBhOn064h32YSss4tXbZ7M43h7UsQ9jsbarlWypTXVdYAp4jpmgjSCtxBfi1Uexv91JU_xkAdSSKyACotoWyGq8Kv9_l-bLVWGqr4JXb9mahMioq_l_7hg8NsR9GQ-F-f4JlgZc7PjWh88neDTsW7QgJBHHUGSv_URA1IS2ctDpGup2jltDC8WYP897DcLVuH8h8EVLecD0qLkR8TwOxaO89wbKORq1J8fI5f7-x877p4ICu1MkwsnkRXqvOc7v28Zwh4tUl2RgRR1DZrJru2kkLLPUu1Bs"",
                "Content-Type": "application/json"
            }

            response = requests.post("https://renewsolutions.ellevo.com/api/v1/ticket", json=payload, headers=headers)

            chamados.append({
                "linha": row.to_dict(),
                "status_code": response.status_code,
                "resposta": response.json() if response.status_code == 200 else response.text
            })

        return jsonify({"resultado": chamados}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
