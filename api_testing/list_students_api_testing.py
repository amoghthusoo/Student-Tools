import requests

url = "http://localhost:8000/api/list_students/"

data = {
    "username" : "gauravsir",
    "course_code" : "CS102",
    "batch" : "2024",
    "session_id" : "bd642c93-1ba2-4092-94a1-9bb437b22e71"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


