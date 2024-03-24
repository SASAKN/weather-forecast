import numpy as np
from keras.models import load_model, Sequential

def predict_model(x, model):
    result = model.predict(x)
    return result

if __name__ == "__main__":
    # モデルの読み込み
    model = load_model('model/model.keras')

    # ランダム配列作成
    test_x = np.random.randint(0, 10, size=(2, 2, 2, 2, 2))

    print(predict_model(test_x, model))
