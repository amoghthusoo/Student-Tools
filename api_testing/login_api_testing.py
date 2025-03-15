import requests

url = "http://127.0.0.1:8000/api/login/"

data = {
    "username" : "amogh",
    "password" : "AmoghThusoo@123"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")