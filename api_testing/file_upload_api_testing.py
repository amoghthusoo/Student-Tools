import requests

url = "http://127.0.0.1:8000/api/upload_file/"

data = {
    "username" : "amogh",
    "session_id" : "1969cb04-c9ad-44f3-9fa0-4970959e5dba"
}

file = {
    "file" : open(r"C:\Users\Dell\Desktop\swd_project\api_testing\test.txt", "rb"),
}

response = requests.post(url, data = data, files = file)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")