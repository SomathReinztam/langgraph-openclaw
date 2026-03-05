import requests

url = "http://localhost:8000/chats/"


chat_model_provider = {
    'client':'google',
    'model':'gemini-3.1-flash-image-preview',
    'temperature':0.2
}

payload = {'user_id':1, 'chat_model_provider':chat_model_provider}

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

