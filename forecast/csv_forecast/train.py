#機械学習
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import ConvLSTM2D, MaxPooling2D, Flatten

#モデルを作成して保存
def save_model():
    model = Sequential()
    model.add(ConvLSTM2D(64, (3, 3), input_shape=())) #input_shapeには、画像の場合だと(width, height, 3)で良い
    model.add(Activation("relu"))
    
    model.save('./model_data/model.h5', overwrite=True, save_format="h5")

#メイン処理
if __name__ == "__main__":
    save_model()
    
