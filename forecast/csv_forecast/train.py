#機械学習
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import ConvLSTM2D, MaxPooling2D, Flatten

def load_ndarray(npz_file):
    return np.load(npz_file)

#モデルを作成して保存
def save_model():
    model = Sequential()
    model.add(ConvLSTM2D(64, (3, 3), input_shape=(155, 215808, 12))) #input_shapeには、画像の場合だと(width, height, 3)で良い
    
    model.save('./model_data/model.h5', overwrite=True, save_format="h5")

#メイン処理
if __name__ == "__main__":
    # 時系列でXとYに分ける

    save_model()
    
