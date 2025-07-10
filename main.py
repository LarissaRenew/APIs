import requests

url = "https://seu-endpoint-ellevo.com/api/tickets"
token = "SEU_TOKEN_AQUI"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
  "title": "Chamado Teste",
  "private": 1,
  "generatorReferenceCode": "usuario123",
  "customerReferenceCode": "cliente001",
  "requesterReferenceCode": "usuario123",
  "serviceReferenceCode": "SERVICO001",
  "responsibleReferenceCode": "GRUPO001",
  "status": "concluded",
  "forms": []
}

resposta = requests.post(url, headers=headers, json=payload)
print(resposta.status_code)
print(resposta.text)
