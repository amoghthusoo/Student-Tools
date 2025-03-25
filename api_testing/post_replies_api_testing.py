import requests

url = "http://localhost:8000/api/post_reply/"

data = {
    "username": "amogh",
    "thread_name": "Teachers' Day Celebration",
    "reply" : "What is the plan for the Teachers' Day celebration?",
    "session_id": "43e16914-9592-4dd9-94ee-161b91720837"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")