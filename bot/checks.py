import requests

PATH = 'http://api:8000/graphql/'

def check_block(chat, chat_id):
    query = """
    query block($number: String!){
        block(number: $number){
            number
        }
    }
    """

    variables = {
            'number': chat[chat_id]['block']
            }

    response = requests.post(PATH, json={'query': query, 'variables':variables})

    return response.json()

def check_apartment(chat, chat_id):
    query = """
    query apartment($number: String!, $block: String!){
        apartment(number: $number, block: $block){
            number
            block{
                number
            }
        }
    }
    """

    variables = {
            'number': chat[chat_id]['apartment'],
            'block': chat[chat_id]['block']
            }

    response = requests.post(PATH, json={'query': query, 'variables':variables})

    return response.json()

def check_email(chat, chat_id):
    query = """
    query user($email: String!){
        user(email: $email){
            completeName
        }
    }
    """

    variables = {
            'email': chat[chat_id]['email']
            }

    response = requests.post(PATH, json={'query': query, 'variables':variables})

    return response.json()

def check_cpf(chat, chat_id):
    query = """
    query user($cpf: String!){
        user(cpf: $cpf){
            completeName
        }
    }
    """

    variables = {
            'cpf': chat[chat_id]['cpf']
            }

    response = requests.post(PATH, json={'query': query, 'variables':variables})

    return response.json()

