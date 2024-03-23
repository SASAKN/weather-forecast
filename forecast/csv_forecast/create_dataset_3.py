import numpy as np
from sklearn.linear_model import LinearRegression

def build_linear_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model

if __name__ == "__main__":
    # データセットの読み込み
    dataset = np.load('./npz_data/dataset.npz')['dataset']

    # 外れ値を含む配列と含まない配列を作成
    outliers = np.where(dataset[:, :, 2] > 10)
    inliers = np.where(dataset[:, :, 2] <= 10)

    # トレーニングデータを作成
    x_train = dataset[outliers[0], outliers[1], 2][:4100900].reshape(-1, 1)
    y_train = dataset[inliers[0], inliers[1], 2][:4100900].reshape(-1, 1)

    # 線形回帰モデルを作成
    model = build_linear_model(x_train, y_train)

    # テストデータを作成
    x_test = dataset[outliers[0], outliers[1], 2].reshape(-1, 1)

    # モデルを使って予測
    y_pred = model.predict(x_test)

    # 予測結果を表示
    print("予測結果:", y_pred)

    # モデルのスコアを計算
    score = model.score(x_test, dataset[outliers[0], outliers[1], 2])
    print("Score:", score)
