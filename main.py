from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

ELLEVO_URL = "https://renewsolutions.ellevo.com/api/v1/ticket"
ELLEVO_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyOTI4NTQ5ODFDNDM4NjBEQkMwREE1OUNCMENDNzk1Mzg3RUNDNDMiLCJ0eXAiOiJKV1QifQ.eyJlbGxldm8vbGFuZ3VhZ2UiOiJwdC1CUiIsImVsbGV2by90ZW5hbnQvaWQiOiI2Mjg1M2UwMDAyNjE5ZjgzMjM1MzYzZWQiLCJlbGxldm8vc3ViLWRvbWFpbiI6InJlbmV3c29sdXRpb25zIiwiZWxsZXZvL3RpbWUtem9uZS1vZmZzZXQiOiItMTgwIiwiZWxsZXZvL2NyZWF0ZWQtYXQiOiI2LzIzLzIwMjUgNTozNzo0NiBQTSIsImlzcyI6IkVsbGV2byIsImF1ZCI6InJlbmV3c29sdXRpb25zIn0.fnuE_UD1ZdmASklBuVrKggDQQyQnmEB_Tp6UsSR7hBeo8bgnQ3FpkFev613zhI0VdRU9EPL6xUCC72BTzi4G2IrTFtN7n8XFSFki6MFE9g9WjjIA6uy6qK3sZmPvgR7nnURrumH0Kd6xZbJJ50aAyrpgans0qEdblXbyWznvKuTBeLjxgZFY2qylJlh0LSmcqnBty-SjxyPNSvCX0lQOqDk3PcRRac6XOR5rLom4aPWugAdRzeoDPuuI7AY-d9InKFoVrFgcfG9X3fkkwh1zsKCdVKJZ2g3cGkhPY3PagHYbfzoTKw7-nHFfOdfvfA18Z8LfBdCTvPYWhXn8Jt7xnPSH_UPdUyd6SV27kqeDaoH88Q1PdDNM-YskzMnZqDKy5vAfdCosYa3UaBhOn064h32YSss4tXbZ7M43h7UsQ9jsbarlWypTXVdYAp4jpmgjSCtxBfi1Uexv91JU_xkAdSSKyACotoWyGq8Kv9_l-bLVWGqr4JXb9mahMioq_l_7hg8NsR9GQ-F-f4JlgZc7PjWh88neDTsW7QgJBHHUGSv_URA1IS2ctDpGup2jltDC8WYP897DcLVuH8h8EVLecD0qLkR8TwOxaO89wbKORq1J8fI5f7-x877p4ICu1MkwsnkRXqvOc7v28Zwh4tUl2RgRR1DZrJru2kkLLPUu1Bs"

def abrir_chamado(dados):
    payload = {
        "title": dados["titulo"],
        "private": 1,
        "generatorReferenceCode": "Solicitante-integracoes-renew",
        "customerReferenceCode": dados["cliente"],
        "requesterReferenceCode": dados["solicitante"],
        "serviceReferenceCode": "TESTE-Integracoes",
        "responsibleReferenceCode": "Grupo-aten-integracao-renew",
        "status": "concluded",
        "dueDate": dados["prazo"],
        "forms": [
            {
                "referenceCode": "FORMULARIO-TESTE-Integracoes",
                "fieldsValues": {
                    "ENTRADADETEXTO-638862167990": dados["texto"],
                    "NUMEROENTERO-638862298298": dados["numero"]
                }
            }
        ]
    }

    headers = {"Authorization": f"Bearer {ELLEVO_TOKEN}"}
    response = requests.post(ELLEVO_URL, json=payload, headers=headers)
    return response.status_code, response.text


@app.route("/abrir-chamado", methods=["POST"])
def processar():
    excel_url = request.json.get("excel_url")
    try:
        df = pd.read_excel(excel_url)
        for _, row in df.iterrows():
            dados = {
                "titulo": row["Titulo"],
                "cliente": row["Cliente"],
                "solicitante": row["Solicitante"],
                "prazo": row["Prazo"],
                "texto": str(row["Texto"]),
                "numero": int(row["Numero"])
            }
            abrir_chamado(dados)
        return jsonify({"mensagem": "Chamados abertos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run()
