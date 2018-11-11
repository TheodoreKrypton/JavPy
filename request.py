import requests

url = "http://www.fembed.com/api/source/dw9re7gzpog"

response = requests.request("POST", url)

print(response.text)