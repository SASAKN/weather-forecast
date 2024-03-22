#機械学習
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dense, Input
from keras.layers import ConvLSTM2D, Flatten, BatchNormalization, Dropout

def build_model():
    # Sequentialモデルを作成
    model = Sequential()

    # 入力層
    model.add(Input(shape=()))

    # 畳み込み層1
    model.add(ConvLSTM2D(filters=64, activation='relu', kernel_size=(5, 5), strides=(1, 1), padding='same', return_sequences=True))
    model.add(BatchNormalization(momentum=0.6))
    model.add(Dropout(0.4))

    # 畳み込み層2
    model.add(ConvLSTM2D(filters=64, activation='relu', kernel_size=(5, 5), strides=(1, 1), padding='same', return_sequences=True))
    model.add(BatchNormalization(momentum=0.6))
    model.add(Dropout(0.4))

    #畳み込み層3
    model.add(ConvLSTM2D(filters=64, activation='relu', kernel_size=(5, 5), strides=(1, 1), padding='same', return_sequences=True))
    model.add(BatchNormalization(momentum=0.6))
    model.add(Dropout(0.4))

    # Flatten層
    model.add(Flatten())
    
    # 隠れ層
    model.add(Dense(units=1, activation='linear'))

    # モデルを作成
    model.compile(optimizer='adam', loss='mse')

    return model



if __name__ == "__main__":
    #モデルを作成
    model = build_model()
    model.save('./model/model.h5')