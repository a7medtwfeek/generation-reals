
import requests
url = "https://api.alquran.cloud/ayah/2:1"
response = requests.get(url)
data = response.json()
print(f"Text: {data['data']['text']}")
print(f"Bytes: {data['data']['text'].encode('utf-8')}")
