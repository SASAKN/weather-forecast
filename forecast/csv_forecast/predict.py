import numpy as np
from keras.models import Sequential
from keras.layers import LSTM

def make_model():
    #Modelを作成
    model = Sequential()
    model.add(LSTM(64, input_shape=(64, 64, 64)))