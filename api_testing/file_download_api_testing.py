import requests

url = "http://127.0.0.1:8000/api/download_file/"


data = {"username" : "amogh",
        "file_name": "test.txt",
        "session_id" : "e5ac2b36-474f-4e6a-8986-d22c2164070f"}  # Send filename in request body

response = requests.post(url, data = data)  # Stream the file

if (response.status_code == 200):
    with open(data["file_name"], "wb") as file:
        file.write(response.content)  # Write the binary response to a file
    print(f"Download complete")

else:
    print(f"Failed to download file: {response.json()}")
