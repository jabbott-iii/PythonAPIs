import requests

url = 'https://jsonplaceholder.typicode.com/posts/1'

response = requests.get(url)

print("Status Code:", response.status_code)
print("Content Type:", response.headers.get('Content-Type'))

data = response.json()
print("Title:", data['title'])
