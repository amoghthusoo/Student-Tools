import requests

url = "http://127.0.0.1:8000/api/logout/"

data = {
    "username" : "amogh",
    "session_id" : "1f50ffca-0d28-44a9-a17b-7e67cd6018d4"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")