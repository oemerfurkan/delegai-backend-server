import requests

url = "https://forum.gnosis.io/t/4717/posts.json"
data = {"url": url}
response = requests.post("http://127.0.0.1:5000/get_tendancy", json=data)

if response.ok:
    result = response.json()
    if result.get('success'):
        print(result['tendancy'])
    else:
        print("Error:", result.get('error'))
else:
    print("Failed to make a request to the API.")