import requests

url = "http://localhost:8000/api/list_threads/"

data = {
    "username": "amogh",
    "session_id": "ff72f07d-1f35-4acd-8908-184f4e8f6ce6"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


