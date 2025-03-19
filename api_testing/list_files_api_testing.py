import requests

url = "http://127.0.0.1:8000/api/list_files/"
# url = "http://student-tools-five.vercel.app/api/login/"

data = {
    "username" : "amogh",
    "session_id" : "1969cb04-c9ad-44f3-9fa0-4970959e5dba"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")