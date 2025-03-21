import requests

url = "http://127.0.0.1:8000/api/keep_alive/"

response = requests.post(url)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
