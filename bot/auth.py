from telegram.ext import ConversationHandler
from python_speech_features import mfcc
from scipy.io.wavfile import read
import json
import numpy
import requests
import subprocess
import logging

logger = logging.getLogger('Alohomora')

CPF_AUTH, VOICE_AUTH = range(2)

PATH = 'http://api:8000/graphql/'

auth_chat = {}

def auth(update, context):
    chat_id = update.message.chat_id
    logger.info("Introducing authentication session")

    update.message.reply_text("Ok, vamos te autenticar!")
    update.message.reply_text("Caso deseje interromper o processo digite /cancelar")
    update.message.reply_text("Por favor, informe seu CPF:")

    logger.info("Asking for CPF")

    auth_chat[chat_id] = {}
    logger.debug("data['%s']: %s" % (chat_id, auth_chat[chat_id]))

    return CPF_AUTH

def cpf_auth(update, context):
    cpf = update.message.text
    chat_id = update.message.chat_id

    if(len(cpf) > 11 and cpf[3] == "." and cpf[7] == "." and cpf[11] == "-"):
        logger.debug("Removing dots and dash from CPF")
        cpf = cpf.replace('.','').replace('-','')

    if(any(i.isalpha() for i in cpf) or "." in cpf or "-" in cpf or len(cpf) != 11):
        logger.error("CPF in wrong formatation - asking again")
        update.message.reply_text('Por favor, digite o CPF com os 11 digitos: (Ex: 123.456.789-10)')
        return CPF_AUTH

    authCPF_J = (int(cpf[0])*10 +
                 int(cpf[1])*9 +
                 int(cpf[2])*8 +
                 int(cpf[3])*7 +
                 int(cpf[4])*6 +
                 int(cpf[5])*5 +
                 int(cpf[6])*4 +
                 int(cpf[7])*3 +
                 int(cpf[8])*2) % 11

    authCPF_K = (int(cpf[0])*11 +
                 int(cpf[1])*10 +
                 int(cpf[2])*9 +
                 int(cpf[3])*8 +
                 int(cpf[4])*7 +
                 int(cpf[5])*6 +
                 int(cpf[6])*5 +
                 int(cpf[7])*4 +
                 int(cpf[8])*3 +
                 int(cpf[9])*2) % 11

    if((int(cpf[9]) != 0 and authCPF_J != 0 and authCPF_J != 1) and (int(cpf[9]) != (11 - authCPF_J))):
        logger.error("Invalid CPF - asking again")
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF_AUTH

    if((int(cpf[10]) != 0 and authCPF_K != 0 and authCPF_K != 1) and (int(cpf[10]) != (11 - authCPF_K))):
        logger.error("Invalid CPF - asking again")
        update.message.reply_text('CPF inválido, tente novamente:')
        return CPF_AUTH

    auth_chat[chat_id]['cpf'] = cpf
    logger.debug("'auth-cpf': '%s'" % auth_chat[chat_id]['cpf'])

    update.message.reply_text('Grave um áudio de no mínimo 1 segundo dizendo "Juro que sou eu"')
    logger.info("Requesting voice audio")

    return VOICE_AUTH

def voice_auth(update, context):
    chat_id = update.message.chat_id
    voice_auth = update.message.voice

    if((voice_auth.duration)<1.0):
        logger.error("Audio too short - asking again")
        update.message.reply_text('Muito curto...O áudio deve ter 1 segundo de duração.')
        update.message.reply_text('Por favor, grave novamente:')
        return VOICE_AUTH
    elif((voice_auth.duration)>2.0):

        logger.error("Audio too long - asking again")
        update.message.reply_text('Muito grande...O áudio deve ter 2 segundo de duração.')
        update.message.reply_text('Por favor, grave novamente:')
        return VOICE_AUTH
    else:
        update.message.reply_text('Ótimo!')

    file_auth = voice_auth.get_file()

    src = file_auth.download()
    dest = src.split('.')[0] + ".wav"

    subprocess.run(['ffmpeg', '-i', src, dest])

    samplerate, voice_data = read(dest)

    mfcc_data = mfcc(voice_data, samplerate=samplerate, nfft=1200, winfunc=numpy.hamming)
    mfcc_data = mfcc_data.tolist()
    mfcc_data = json.dumps(mfcc_data)

    auth_chat[chat_id]['voice_mfcc'] = mfcc_data
    logger.debug("'auth-voice-mfcc': %s...%s" % (auth_chat[chat_id]['voice_mfcc'][:5], auth_chat[chat_id]['voice_mfcc'][-5:]))

    response = authenticate(chat_id)

    valid = response['data']['voiceBelongsUser']

    if valid:
        logger.info("User has been authenticated")
        update.message.reply_text('Autenticado(a) com sucesso!')
    else:
        logger.error("Authentication failed")
        update.message.reply_text('Falha na autenticação!')

    auth_chat[chat_id] = {}

    return ConversationHandler.END

def end_auth(update, context):
    logger.info("Canceling authentication")

    chat_id = update.message.chat_id
    update.message.reply_text('Autenticação cancelada!')

    auth_chat[chat_id] = {}

    return ConversationHandler.END

def authenticate(chat_id):
    logger.info("Authenticating user")

    query = """
    query voiceBelongsUser(
        $cpf: String!,
        $mfccData: String
    ){
        voiceBelongsUser(cpf: $cpf, mfccData: $mfccData)
    }
    """

    variables = {
            'cpf': auth_chat[chat_id]['cpf'],
            'mfccData': auth_chat[chat_id]['voice_mfcc']
    }

    response = requests.post(PATH, json={'query':query, 'variables':variables})

    logger.debug("Response: " + str(response.json()))

    return response.json()

