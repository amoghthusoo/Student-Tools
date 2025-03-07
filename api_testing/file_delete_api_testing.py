import requests

url = "http://127.0.0.1:8000/api/delete_file/"

data = {
    "username" : "amogh",
    "file_name" : "form.pdf",
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
