import requests

url = "http://127.0.0.1:8000/api/upload_file/"

data = {
    "username" : "amogh",
    "session_id" : "eca2b355-adb5-4654-bb2a-7fcca13a7635"
}

file = {
    "file" : open(r"C:\Users\Dell\Desktop\swd_project\api_testing\test.txt", "rb"),
}

response = requests.post(url, data = data, files = file)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")