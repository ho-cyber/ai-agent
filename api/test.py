import requests

# URL of the API
base_url = 'http://localhost:3000/chat'

# Demo user ID
user_id = 'Dhruv'

# GET request to retrieve chat history for demo_user
response = requests.get(f'{base_url}/{user_id}')
if response.status_code == 200:
    chat_history = response.json()['chatHistory']
    print('Chat History:')
    for chat in chat_history:
        print(chat['message'])
else:
    print('Error retrieving chat history')
