import requests

url = "http://localhost:8000/api/add_student/"

data = {
    "username" : "amogh",
    "course_code" : "CS102",
    "student_username" : "umang",
    "batch" : "2024",
    "mac_address" : "00:1A:2B:3C:4D:5E",
    "session_id" : "887eb5c9-5b1e-4f79-b73a-661b4d49f068"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


