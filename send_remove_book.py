import requests
import json

def remove_book(title):

    url = "http://localhost:5001/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "titleDelete": title
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Resposta do servidor: ", response.json())

    else :
        print("Erro: ", response.json())


if __name__ == "__main__":
    remove_book("O Senhor dos Anéis")
