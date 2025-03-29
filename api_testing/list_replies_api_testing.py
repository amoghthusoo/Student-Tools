import requests

url = "http://localhost:8000/api/list_replies/"

data = {
    "thread_name" : "Hackathon 2025",
    "username": "amogh",
    "session_id": "6c64a9ec-db25-41ab-b397-cbaff6e06344",
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


