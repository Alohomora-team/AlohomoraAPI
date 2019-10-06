import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from auth import auth, cpf_auth, voice_auth, end_auth
from register import register, name, phone, email, cpf, apartment, block, voice_register, repeat_voice, end

PATH = 'http://api:8000/graphql/'
NAME, PHONE, EMAIL, CPF, BLOCK, APARTMENT, VOICE_REGISTER, REPEAT_VOICE = range(8)
CPF_AUTH, VOICE_AUTH = range(2)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Olá, bem vindo(a) ao bot do Alohomora!')
    update.message.reply_text('Digite /cadastrar para fazer o cadastro de um morador')
    update.message.reply_text('Caso deseje fazer a autenticação por voz, digite /autenticar')


if __name__ == '__main__':

    token = '959215527:AAG3K2izQIOGmi82pwFnWyGvr0flkq0K3do'

    updater = Updater(token, use_context=True)

    logging.info("Iniciando Bot")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Registration
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('cadastrar', register, pass_args=True)],

        states={
            NAME:[MessageHandler(Filters.text, name)],
            PHONE:[MessageHandler(Filters.text | Filters.contact, phone)],
            EMAIL:[MessageHandler(Filters.text, email)],
            CPF:[MessageHandler(Filters.text, cpf)],
            APARTMENT:[MessageHandler(Filters.text, apartment)],
            BLOCK:[MessageHandler(Filters.text, block)],
            VOICE_REGISTER: [MessageHandler(Filters.voice, voice_register)],
            REPEAT_VOICE:[MessageHandler(Filters.text, repeat_voice)]
            },

        fallbacks=[CommandHandler('cancelar', end)]
        ))

    # Authentication
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('autenticar', auth)],

        states={
            CPF_AUTH:[MessageHandler(Filters.text, cpf_auth)],
            VOICE_AUTH: [MessageHandler(Filters.voice, voice_auth)]
            },

        fallbacks=[CommandHandler('cancelar', end_auth)]
        ))


    updater.start_polling()

    updater.idle()
