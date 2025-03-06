import requests

url = "http://127.0.0.1:8000/api/upload_file/"

data = {
    "username" : "amogh",
}

file = {
    "file" : open(r"C:\Users\Dell\Desktop\swd_project\api_testing\ch01 Introduction.ppt", "rb"),
}

response = requests.post(url, data = data, files = file)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
