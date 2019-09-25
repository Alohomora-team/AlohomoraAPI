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
    data['email'] = email

    update.message.reply_text('Senha:')
    return PASSWORD
def password(update, context):
    password = update.message.text
    data['password'] = password

    update.message.reply_text('CPF:')
    return CPF
def cpf(update, context):
    cpf = update.message.text
    data['cpf'] = cpf

    update.message.reply_text('Apartamento:')
    return APARTMENT
def apartment(update, context):
    apartment = update.message.text
    data['apartment'] = apartment

    update.message.reply_text('Bloco:')
    return BLOCK
def block(update, context):
    block = update.message.text
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
            PHONE:[MessageHandler(Filters.text, phone)],
            EMAIL:[MessageHandler(Filters.text | Filters.contact, email)],
            PASSWORD:[MessageHandler(Filters.text, password)],
            CPF:[MessageHandler(Filters.text, cpf)],
            APARTMENT:[MessageHandler(Filters.text, apartment)],
            BLOCK:[MessageHandler(Filters.text, block)]
            },

        fallbacks=[CommandHandler('end', end)]
        ))

    updater.start_polling()

    updater.idle()
