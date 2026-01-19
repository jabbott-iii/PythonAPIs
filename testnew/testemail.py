import requests

url = 'https://reqres.in/api/users/'
params = {'page': 2} # Example query parameter

response = requests.get(url, params=params) # Send GET request with parameters
print('Final URL:', response.url)

response.raise_for_status()  # Raise an error for bad responses

data = response.json() # Parse JSON response

for user in data.get('data', []): # Iterate through user data
    print(f"ID: {user['id']}, Email: {user['email']}")