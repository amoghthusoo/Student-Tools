import requests

url = "http://localhost:8000/api/list_attendance/"

data = {
    "username" : "umang",
    "session_id" : "fbd40f29-a4af-4c57-bcca-c31fc6584830"
}

response = requests.post(url, data=data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")


