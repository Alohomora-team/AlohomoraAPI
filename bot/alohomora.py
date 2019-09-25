import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

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

    update.message.reply_text('Telefone:')
    return PHONE
def phone(update, context):
    phone = update.message.text

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

    update.message.reply_text('Morador cadastrado no sistema!')
    print(data)
    return ConversationHandler.END
def end(update, context):
    update.message.reply_text('Cancelando cadastro!')
    data = {}
    return ConversationHandler.END

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
