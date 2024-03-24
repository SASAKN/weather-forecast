#機械学習
import numpy as np
from keras.models import load_model, Sequential
from sklearn.model_selection import train_test_split

def fit_model(x, y, model):
    model.fit(x, y, epochs=100)


if __name__ == "__main__":
    #モデルをロード
    model = load_model('model/model.keras')

    #データを用意
    x = np.random.randint(0, 10, size=(2, 2, 2, 2, 2))
    y = np.random.randint(0, 100, size=(2, 2, 2, 2, 2))
    train_x, train_y, test_x, test_y = train_test_split(x, y, train_size=0.8)
    fit_model(train_x, train_y, model)

    # もう一度保存
    model.save('model/model.keras')

