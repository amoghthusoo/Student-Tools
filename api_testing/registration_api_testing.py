import requests

url = "http://127.0.0.1:8000/api/registration/"

data = {
    "username" : "swdproject2025user2",
    "password" : "hello123",
    "email" : "swdproject2025user1@gmail.com",
    "is_student" : True,
    "otp" : 447063
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")