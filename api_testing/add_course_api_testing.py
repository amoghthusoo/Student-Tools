import requests

url = "http://localhost:8000/api/add_course/"

data = {
    "username" : "amogh",
    "course_code" : "CS102",
    "course_name" : "Computer Science 102",
    "batch" : "2024",
    "session_id" : "887eb5c9-5b1e-4f79-b73a-661b4d49f068"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


