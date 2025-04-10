import requests

url = "http://localhost:8000/api/get_attendance_report/"

data = {
    "username" : "gauravsir",
    "course_code" : "CS102",
    "batch" : "2024",
    "session_id" : "b8e27e37-de14-4313-a589-e380703dc708"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


