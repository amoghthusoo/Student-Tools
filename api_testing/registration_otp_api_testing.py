import requests

# url = "http://127.0.0.1:8000/api/generate_registration_otp/"
url = "https://student-tools-gules.vercel.app/api/generate_registration_otp/"

data = {
    "email" : "2022btcse007@curaj.ac.in"
}

response = requests.post(url, data = data)

print(f"Status Code : {response.status_code}")
print(f"Response JSON : {response.json()}")
