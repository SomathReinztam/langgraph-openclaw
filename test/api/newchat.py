import requests

url = "http://localhost:8000/chats/"


payload = {
    'client':'google',
    'model':'admin@admin.com',
    'temperature':0.2
}


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

