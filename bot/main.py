import logging
import requests
import numpy
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

from telegram import KeyboardButton, ReplyKeyboardMarkup

path = 'http://api:8000/graphql/'


NAME, PHONE, EMAIL, PASSWORD, CPF, BLOCK, APARTMENT, VOICE_REGISTER = range(8)

data = {}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Olá, bem vindo(a) ao bot do Alohomora!')
    update.message.reply_text('Digite /cadastrar para fazer o cadastro de um morador')

def register(update, context):
    update.message.reply_text('Ok, vamos iniciar o cadastro!')
    update.message.reply_text('Caso deseje interromper o processo digite /cancelar')
    update.message.reply_text('Nome:')

    return NAME

def name(update, context):
    name = update.message.text

    if("nome" in name.lower()):
        update.message.reply_text('Por favor, digite apenas o seu nome: (Ex: João da Silva)')
        return NAME
    if(any(i.isdigit() for i in name)):
        update.message.reply_text('Por favor, não digite números no nome, tente novamente:')
        return NAME
    if("@" in name or len(name)<3):
        update.message.reply_text('Neste momento é hora de digitar o seu nome, tente novamente:')
        return NAME
    if(len(name) > 80):
        update.message.reply_text('Nome excedeu tamanho máximo (80), tente novamente:')
        return NAME

    data['name'] = name

    contact_keyboard = KeyboardButton('Enviar meu número de telefone', request_contact=True)
    custom_keyboard = [[ contact_keyboard ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text('Telefone:', reply_markup=reply_markup)
    return PHONE

def phone(update, context):
    if(update.message.text is not None):
        phone = update.message.text

        if("-" in phone):
            phone = phone.replace('-','')

        if(" " in phone):
            phone = phone.replace(' ','')

        if("+" in phone):
            phone = phone.replace('+','')

        if(any(i.isalpha() for i in phone)):
            update.message.reply_text('Por favor, digite seu telefone corretamente:')
            return PHONE

        if(len(phone) > 15):
            update.message.reply_text('Telefone excedeu tamanho máximo (15), tente novamente:')
            return PHONE

    else:
        contact = update.effective_message.contact
        phone = contact.phone_number
        phone = phone.replace('+','')

    data['phone'] = phone

    update.message.reply_text('Email:')
    return EMAIL

def email(update, context):
    email = update.message.text

    if("@" not in email or " " in email or len(email)<4 or "." not in email):
        update.message.reply_text('Por favor, digite um email válido:')
        return EMAIL

    if(len(email) > 90):
        update.message.reply_text('Email excedeu tamanho máximo (90), tente novamente:')
        return EMAIL

    data['email'] = email

    check = check_email()

    if 'errors' not in check.keys():
        update.message.reply_text('Já existe um morador com este email, tente novamente:')
        return EMAIL

    update.message.reply_text('Senha:')
    return PASSWORD

def password(update, context):
    password = update.message.text

    if(len(password)<4 or len(password)>10):
        update.message.reply_text('Por favor, digite uma senha de 4~10 caracteres:')
        return PASSWORD

    data['password'] = password

    update.message.reply_text('CPF:')
    return CPF

def cpf(update, context):
    cpf = update.message.text

    if(len(cpf) > 11 and cpf[3] == "." and cpf[7] == "." and cpf[11] == "-"):
        cpf = cpf.replace('.','').replace('-','')

    if(any(i.isalpha() for i in cpf) or "." in cpf or "-" in cpf or len(cpf) != 11):
        update.message.reply_text('Por favor, digite o CPF com os 11 digitos: (Ex: 123.456.789-10)')
        return CPF

    authCPF_J = (int(cpf[0])*10 + int(cpf[1])*9 + int(cpf[2])*8 + int(cpf[3])*7 + int(cpf[4])*6 + int(cpf[5])*5 + int(cpf[6])*4 + int(cpf[7])*3 + int(cpf[8])*2)%11
    authCPF_K = (int(cpf[0])*11 + int(cpf[1])*10 + int(cpf[2])*9 + int(cpf[3])*8 + int(cpf[4])*7 + int(cpf[5])*6 + int(cpf[6])*5 + int(cpf[7])*4 + int(cpf[8])*3 + int(cpf[9])*2)%11

    if((int(cpf[9]) != 0 and authCPF_J != 0 and authCPF_J != 1) and (int(cpf[9]) != (11 - authCPF_J))):
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF

    if((int(cpf[10]) != 0 and authCPF_K != 0 and authCPF_K != 1) and (int(cpf[10]) != (11 - authCPF_K))):
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF

    data['cpf'] = cpf

    check = check_cpf()

    if 'errors' not in check.keys():
        update.message.reply_text('Já existe um morador com este CPF, tente novamente:')
        return CPF
    
    update.message.reply_text('Bloco:')
    return BLOCK

def block(update, context):
    block = update.message.text

    if("bloco" in block.lower() or " " in block):
        update.message.reply_text('Por favor, digite apenas o bloco: (Ex: 1)')
        return BLOCK

    if(len(block) > 4):
        update.message.reply_text('Digte um bloco de até 4 caracteres:')
        return BLOCK

    data['block'] = block

    check = check_block()

    if 'errors' in check.keys():
        update.message.reply_text('Por favor, digite um bloco existente:')
        return BLOCK

    update.message.reply_text('Apartamento:')
    return APARTMENT

def apartment(update, context):
    apartment = update.message.text

    if(any(i.isalpha() for i in apartment) or " " in apartment):
        update.message.reply_text('Por favor, digite apenas o apartamento: (Ex: 101)')
        return APARTMENT

    if(len(apartment) > 6):
        update.message.reply_text('Digite um apartamente de até 6 caracteres:')
        return APARTMENT

    data['apartment'] = apartment

    check = check_apartment()

    if 'errors' in check.keys():
        update.message.reply_text('Por favor, digite um apartamento existente:')
        return APARTMENT

    update.message.reply_text('Vamos agora cadastrar a sua frase! Grave uma mensagem de voz com a sua frase:')
    return VOICE_REGISTER

def voice_register(update, context):
    voice_register = update.message.voice

    if((voice_register.duration)<2):
        update.message.reply_text('Muito curto...O áudio deve ter 2 segundos de duração.')
        update.message.reply_text('Por favor, grave novamente:')
        return VOICE_REGISTER
    else:
        update.message.reply_text('Ótimo! Não esqueça da sua frase: mais pra frente você precisará dela!')

    f_reg = voice_register.get_file()
    file_barr = f_reg.download_as_bytearray()

    del file_barr[5788:len(file_barr)]

    audio_arr_reg = numpy.frombuffer(file_barr, dtype="float32")
    voice_data_reg = json.dumps(audio_arr_reg.tolist())

    data['voice_reg'] = voice_data_reg


    response = register_user()

    if(response.status_code == 200):
        update.message.reply_text('Morador cadastrado no sistema!')
    else:
        update.message.reply_text('Falha ao cadastrar no sistema!')

    return ConversationHandler.END

def end(update, context):
    update.message.reply_text('Cadastro cancelado!')
    data = {}
    return ConversationHandler.END

def register_user():
    print(data)

    query_user = """
    mutation createUser($completeName: String!, $email: String!, $password: String!, $phone: String!, $cpf: String!, $apartment: String!, $block: String!, $voiceData: String!){
        createUser(
            completeName: $completeName,
            email: $email,
            password: $password,
            cpf: $cpf,
            phone: $phone,
            apartment: $apartment,
            block: $block,
            voiceData: $voiceData
        ){
            user{
                completeName
                email
                cpf
                phone
                apartment{
                    number
                    block{
                        number
                    }
                }
                voiceData
            }
        }
    }
    """

    variables_user = {
            'completeName': data['name'],
            'email': data['email'],
            'password': data['password'],
            'phone': data['phone'],
            'cpf': data['cpf'],
            'apartment': data['apartment'],
            'block': data['block'],
            'voiceData': data['voice_reg']
            }

    user_response = requests.post(path, json={'query':query_user, 'variables':variables_user})


    print("status code: " + str(user_response.status_code))
    print(user_response.json())

    return user_response

def check_block():
    query = """
    query block($number: String!){
        block(number: $number){
            number
        }
    }
    """

    variables = {
            'number': data['block']
            }

    response = requests.post(path, json={'query': query, 'variables':variables})

    return response.json()

def check_apartment():
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
            'number': data['apartment'],
            'block': data['block']
            }

    response = requests.post(path, json={'query': query, 'variables':variables})

    return response.json()

def check_email():
    query = """
    query user($email: String!){
        user(email: $email){
            completeName
        }
    }
    """

    variables = {
            'email': data['email']
            }

    response = requests.post(path, json={'query': query, 'variables':variables})

    return response.json()

def check_cpf():
    query = """
    query user($cpf: String!){
        user(cpf: $cpf){
            completeName
        }
    }
    """

    variables = {
            'cpf': data['cpf']
            }

    response = requests.post(path, json={'query': query, 'variables':variables})

    return response.json()

if __name__ == '__main__':

    token = '959215527:AAG3K2izQIOGmi82pwFnWyGvr0flkq0K3do'

    updater = Updater(token, use_context=True)

    print("Iniciando Bot")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('cadastrar', register)],

        states={
            NAME:[MessageHandler(Filters.text, name)],
            PHONE:[MessageHandler(Filters.text | Filters.contact, phone)],
            EMAIL:[MessageHandler(Filters.text, email)],
            PASSWORD:[MessageHandler(Filters.text, password)],
            CPF:[MessageHandler(Filters.text, cpf)],
            APARTMENT:[MessageHandler(Filters.text, apartment)],
            BLOCK:[MessageHandler(Filters.text, block)],
            VOICE_REGISTER: [MessageHandler(Filters.voice, voice_register)]
            },

        fallbacks=[CommandHandler('cancelar', end)]
        ))

    updater.start_polling()

    updater.idle()