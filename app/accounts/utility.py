import json
import numpy
from python_speech_features import mfcc
from fastdtw import fastdtw

def json_to_numpy_array(voice_data):
    voice_data = json.loads(voice_data)
    voice_data = numpy.array(voice_data)

    return voice_data

def numpy_array_to_json(voice_data):
    voice_data = voice_data.tolist()
    voice_data = json.dumps(voice_data)

    return voice_data

def json_voice_data_to_mfcc(voice_data):
    voice_data = json_to_numpy_array(voice_data)
    voice_data = mfcc(voice_data, samplerate=16000)

    return voice_data

def json_voice_data_to_json_mfcc(voice_data):
    voice_data = json_voice_data_to_mfcc(voice_data)
    voice_data = numpy_array_to_json(voice_data)

    return voice_data

def compute_dtw_distance(serie1, serie2):
    distance, _ignored = fastdtw(serie1, serie2)

    return distance
    