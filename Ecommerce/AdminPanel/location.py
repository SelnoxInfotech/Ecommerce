import requests

# key="AIzaSyCroMqCji7d1lMYSEGOmuF_FOi2Na9I-0Q"
origin=str(input("Origin"))
# destination=input("Destination")
url = "https://maps.googleapis.com/maps/api/directions/json?",origin,"=newyork&destination=brooklyn&key=AIzaSyCroMqCji7d1lMYSEGOmuF_FOi2Na9I-0Q"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)