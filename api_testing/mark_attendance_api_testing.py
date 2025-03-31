import requests

url = "http://localhost:8000/api/mark_attendance/"

data = {
    "username" : "amogh",
    "course_code" : "CS102",
    "batch" : "2024",
    "students" : {
        "umang" : False,
    },
    "session_id" : "887eb5c9-5b1e-4f79-b73a-661b4d49f068"
}

response = requests.post(url, json = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


