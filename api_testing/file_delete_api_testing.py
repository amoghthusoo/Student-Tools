import requests

url = "http://127.0.0.1:8000/api/delete_file/"

data = {
    "username" : "amogh",
    "file_name" : "test.txt",
    "session_id" : "e5ac2b36-474f-4e6a-8986-d22c2164070f"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
