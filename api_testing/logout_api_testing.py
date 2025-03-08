import requests

url = "http://127.0.0.1:8000/api/logout/"

data = {
    "username" : "amogh",
    "session_id" : "63d604e7-fd09-4726-a835-a3d964e952ad"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")