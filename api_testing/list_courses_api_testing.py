import requests

url = "http://localhost:8000/api/list_courses/"

data = {
    "username" : "gauravsir",
    "session_id" : "b17c8759-b824-4733-8b86-f95aa3b20030"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


