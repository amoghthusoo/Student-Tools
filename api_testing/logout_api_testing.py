import requests

url = "http://127.0.0.1:8000/api/logout/"

data = {
    "username" : "amogh",
    "session_id" : "423846be-3e48-484e-a319-020946f2412f"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")