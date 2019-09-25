import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

from telegram import KeyboardButton, ReplyKeyboardMarkup

NAME, PHONE, EMAIL, PASSWORD, CPF, APARTMENT, BLOCK = range(7)

data = {}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Olá, bem vindo(a) ao bot do Alohomora!')
    update.message.reply_text('Digite /cadastrar para fazer o cadastro de um morador')

def register(update, context):
    update.message.reply_text('Certo, vamos iniciar o cadastro!')
    update.message.reply_text('Nome:')

    return NAME
def name(update, context):
    name = update.message.text

    if("nome" in name.lower()):
        update.message.reply_text('Por favor, digite apenas o seu nome: (Ex: João da Silva)')
        return NAME
    elif(any(i.isdigit() for i in name)):
        update.message.reply_text('Por favor, não digite números no nome, tente novamente:')
        return NAME
    elif("@" in name or len(name)<3):
        update.message.reply_text('Neste momento é hora de digitar o seu nome, tente novamente:')
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

        if(any(i.isalpha() for i in phone)):
            update.message.reply_text('Por favor, digite seu telefone corretamente:')
            return PHONE

    else:
        contact = update.effective_message.contact
        phone = contact.phone_number

    data['phone'] = phone

    update.message.reply_text('Email:')
    return EMAIL
def email(update, context):
    email = update.message.text

    if("@" not in email or " " in email or len(email)<4):
        update.message.reply_text('Por favor, digite seu email corretamente:')
        return EMAIL

    data['email'] = email

    update.message.reply_text('Senha:')
    return PASSWORD
def password(update, context):
    password = update.message.text

    if(len(password)<4):
        update.message.reply_text('Por favor, digite uma senha com no mínimo 4 caractéres:')
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
    print(authCPF_J)
    print(authCPF_K)

    if((int(cpf[9]) != 0 and authCPF_J != 0 and authCPF_J != 1) and (int(cpf[9]) != (11 - authCPF_J))):
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF

    if((int(cpf[10]) != 0 and authCPF_K != 0 and authCPF_K != 1) and (int(cpf[10]) != (11 - authCPF_K))):
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF


    data['cpf'] = cpf

    update.message.reply_text('Apartamento:')
    return APARTMENT
def apartment(update, context):
    apartment = update.message.text

    if(any(i.isalpha() for i in apartment) or " " in apartment):
        update.message.reply_text('Por favor, digite apenas o apartamento: (Ex: 101)')
        return APARTMENT

    data['apartment'] = apartment

    update.message.reply_text('Bloco:')
    return BLOCK
def block(update, context):
    block = update.message.text

    if("bloco" in block.lower() or " " in block):
        update.message.reply_text('Por favor, digite apenas o bloco: (Ex: 1)')
        return BLOCK

    data['block'] = block

   
    response = register_user()
    
    if(response.status_code == 200):
        update.message.reply_text('Morador cadastrado no sistema!')
    else:
        update.message.reply_text('Falha ao cadastrar no sistema!')

    return ConversationHandler.END
def end(update, context):
    update.message.reply_text('Cancelando cadastro!')
    data = {}
    return ConversationHandler.END

def register_user():
    path = 'http://127.0.0.1:8000/graphql/'
    print(data)

    query_user = """
    mutation createUser($completeName: String!, $email: String!, $password: String!, $phone: String!, $cpf: String!, $apartment: String!, $block: String!){
        createUser(
            completeName: $completeName,
            email: $email,
            password: $password,
            cpf: $cpf,
            phone: $phone,
            apartment: $apartment,
            block: $block
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
            'block': data['block']
            }
    
    user_response = requests.post(path, json={'query':query_user, 'variables':variables_user})


    print("status code: " + str(user_response.status_code))
    print(user_response.json())

    return user_response


if __name__ == '__main__':

    token = '959215527:AAG3K2izQIOGmi82pwFnWyGvr0flkq0K3do'

    updater = Updater(token, use_context=True)

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
            BLOCK:[MessageHandler(Filters.text, block)]
            },

        fallbacks=[CommandHandler('end', end)]
        ))

    updater.start_polling()

    updater.idle()
