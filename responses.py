import requests
import random

response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})

if response.status_code == 200:
    data = response.json()
    # print(data['joke'])
else:
    print('An error occurred while retrieving the joke.')


def get_random_joke():
    response = requests.get('https://icanhazdadjoke.com/search', headers={'Accept': 'application/json'},
                            params={'limit': 30})
    if response.status_code == 200:
        data = response.json()
        if len(data['results']) > 0:
            joke = random.choice(data['results'])['joke']
            return joke
        else:
            return 'No jokes found. Try again later.'
    else:
        return 'An error occurred while retrieving the joke.'


def handle_response(message: str, display_name: str) -> str:
    p_message = message.lower().strip()

    if p_message == 'hello':
        return f'Hello {display_name} '

    if p_message == 'sup bitch':
        return f'sup {display_name} you dumbass bitch'

    if p_message == 'bitch':
        return '***BITCH***'

    if p_message == 'youre a bitch':
        return 'how dare you'

    if p_message == 'are you cute?':
        return 'bitch im serving cunt'

    if p_message == 'faggot':
        return 'youre an enabler'

    if p_message == 'tell me a joke':
        return get_random_joke()

    if p_message == 'fuck you':
        return f'fuck you {display_name} you raggedy bitch'

    else:
        return 'what bitch'


