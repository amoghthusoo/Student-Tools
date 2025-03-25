import requests

url = "http://localhost:8000/api/delete_thread/"

data = {
    "username": "amogh",
    "thread_name": "Teacher's Day",
    "session_id": "bf6e4941-048d-426e-aaac-60bd267dee83"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


