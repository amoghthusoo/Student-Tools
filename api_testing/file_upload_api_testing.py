import requests

url = "http://127.0.0.1:8000/api/upload_file/"

data = {
    "username" : "amogh",
    "session_id" : "e5ac2b36-474f-4e6a-8986-d22c2164070f"
}

file = {
    "file" : open(r"C:\Users\Dell\Desktop\swd_project\api_testing\test.txt", "rb"),
}

response = requests.post(url, data = data, files = file)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
