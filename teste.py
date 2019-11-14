import app.accounts.utility as util
from python_speech_features import mfcc
import numpy

a = [x*x + x + 300 for x in range(32073)]
mfcc_matrix = mfcc(numpy.array(a), 16000, winfunc=numpy.hamming)

mfcc_array = util.mfcc_matrix_to_array(mfcc_matrix)
mfcc_matrix_2 = util.mfcc_array_to_matrix(mfcc_array)

assert mfcc_matrix.all() == numpy.array(mfcc_matrix_2).all()