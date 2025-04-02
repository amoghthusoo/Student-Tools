import requests

url = "http://localhost:8000/api/list_attendance/"

data = {
    "username" : "amogh",
    "session_id" : "26dbac44-f0a4-412e-b541-84ae893f3d17"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


