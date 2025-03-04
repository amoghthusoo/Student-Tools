import requests

url = "http://127.0.0.1:8000/api/login/"

data = {
    "username" : "swdproject2025user1",
    "password" : "hello_world"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")