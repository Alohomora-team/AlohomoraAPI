"""Module for grouping utility functions used throughout the project"""
import os
import json
import string
import random
import numpy
from scipy.io.wavfile import read, write
from python_speech_features import mfcc
from fastdtw import fastdtw

def json_to_numpy_array(voice_data):
    """Converts JSON object to numpy array"""
    voice_data = json.loads(voice_data)
    voice_data = numpy.array(voice_data)

    return voice_data

def numpy_array_to_json(voice_data):
    """Converts numpy arrays to JSON objects"""
    voice_data = voice_data.tolist()
    voice_data = json.dumps(voice_data)

    return voice_data

def json_voice_data_to_mfcc(voice_data):
    """Converts JSON object to MFCCs"""
    voice_data = json_to_numpy_array(voice_data)
    voice_data = mfcc(voice_data, samplerate=16000)

    return voice_data

def json_voice_data_to_json_mfcc(voice_data):
    """Converts JSON object to JSON represantation of MFCCs"""
    voice_data = json_voice_data_to_mfcc(voice_data)
    voice_data = numpy_array_to_json(voice_data)

    return voice_data

def compute_dtw_distance(serie1, serie2):
    """Returns the Dynamic time warping distance"""
    distance, _ignored = fastdtw(serie1, serie2)

    return distance

def mfcc_matrix_to_array(mfcc_matrix):
    '''
    Transform a mfcc_matrix into a mfcc_array.

    mfcc_array will be an array such that rows is abstracted in columns,
    i.e. mfcc_matrix:[[1,2,3,4,5,6,7,8,9,10,11,12,13], [14,15,16,17,18,19,20,21,22,23,24,25,26]]
         mfcc_array: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],

    :param mfcc_matrix: the mfcc data matrix
    :returns: a list "mfcc_array"
    '''

    mfcc_array = list()
    for line in mfcc_matrix:
        mfcc_array += list(line)

    return mfcc_array

def mfcc_array_to_matrix(mfcc_array):
    '''
    Transform a mfcc_array into a mfcc_matrix.

    mfcc_array should be an array such that rows is abstracted in columns,
    i.e. mfcc_array: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
         mfcc_matrix:[[1,2,3,4,5,6,7,8,9,10,11,12,13], [14,15,16,17,18,19,20,21,22,23,24,25,26]]

    :param mfcc_array: the mfcc data array
    :returns: a list of lists "mfcc_matrix"
    '''
    column_length, array_len = 13, len(mfcc_array)
    mfcc_matrix = [mfcc_array[x:x + column_length] for x in range(0, array_len, column_length)]

    return mfcc_matrix

def create_model_mfcc(audio_signal, samplerate):
    """
    Create a linearized matrix of audio_signal's MFCC

    :param auio_signal: Audio signal array
    :param samplerate: audio_signal's samplerate
    :returns: audio_signal's MFCC linearized matrix
    """

    mfcc_audio_signal = mfcc(
        numpy.array(audio_signal),
        samplerate=samplerate,
        winfunc=numpy.hamming
    )

    return mfcc_matrix_to_array(mfcc_audio_signal)

def create_model_mfcc_from_wav_file(file_path):
    '''
    Create a linearized matrix of MFCCs from a audio file

    :param file_path: a string containing the file path
    :returns: MFCCs linearized matrix
    '''
    treat_audio_file(file_path)
    samplerate, data = read(file_path)
    return create_model_mfcc(data, samplerate)

def treat_audio_file(file_path):
    '''
    Remove noise, silence and unnecessary frequencies from wav audio file

    :param file_path: a string containing the file path
    :returns: None
    '''
    file_name = file_path.split('/')[-1].split('.')[0]

    os.system(f"sox {file_path} -n trim 0 0.4 noiseprof {file_name}.noise-profile")
    os.system(f"sox {file_path} {file_name}_tmp.wav noisered {file_name}.noise-profile 0.26")
    os.system(f"sox {file_name}_tmp.wav {file_path} highpass 300 lowpass 3400")
    os.system(f"sox {file_path} {file_name}_tmp.wav silence 1 1 2 reverse silence 1 1 1 reverse")
    os.system(f"sox {file_name}_tmp.wav {file_path} rate 16k")

    os.system(f"rm {file_name}_tmp.wav {file_name}.noise-profile")

    return None

def treat_audio_data(audio_data, samplerate):
    '''
    Remove noise, silence and unnecessary frequencies from audio data array

    :param audio_data: an array containing audio data
    :returns: treated array containing audio data
    '''
    # letters = string.ascii_lowercase
    # tmp_file_path = ''.join(random.choice(letters) for i in range(10))
    # tmp_file_path = tmp_file_path + '.wav'
    tmp_file_path = 'tmp_audio.wav'

    write(tmp_file_path, samplerate, numpy.array(audio_data))
    treat_audio_file(tmp_file_path)

    samplerate, data = read(tmp_file_path)
    os.system(f"rm {tmp_file_path}")

    return data
