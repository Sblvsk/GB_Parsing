import requests
import json


url = "https://api.github.com/users/Sblvsk/repos"
session = requests.Session()
response = session.get(url)
data = response.json()
names = [data[i]['name'] for i in range(len(data))]

with open('end.json', 'w', encoding="UTF-8") as f:
    json.dump(data,f)

