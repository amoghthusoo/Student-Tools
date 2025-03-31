import requests

url = "http://127.0.0.1:8000/api/list_files/"
# url = "http://student-tools-five.vercel.app/api/login/"

data = {
    "username" : "amogh",
    "session_id" : "887eb5c9-5b1e-4f79-b73a-661b4d49f068"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")