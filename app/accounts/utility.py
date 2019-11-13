"""Module for grouping utility functions used throughout the project"""
import json
import numpy
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
        