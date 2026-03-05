import requests

url = "http://localhost:8000/runeduchat/"

payload = {
    "user_id": 1,
    "chat_id": 1,
    "human_message": "Cual es el estado de los proyectos en fase de construccion y si vamps a alcanzar a tenerlo listo antes de los tiempos previstos ?",
}
# "system_prompt": "algun system prompt"

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Respuesta:")
    print(data)
else:
    print("Error:")
    print(response.text)

