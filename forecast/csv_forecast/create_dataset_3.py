import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
import copy
import warnings

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

    # 外れ値のインデックスをランダムに選択
    outlier_indices = np.random.choice(len(outliers[0]), size=1000, replace=False)

    # トレーニングデータを作成
    x_train = dataset[inliers[0], inliers[1], 2].reshape(-1, 1)
    y_train = dataset[inliers[0], inliers[1], 2]

    # 外れ値を含むデータを除外
    x_train = np.delete(x_train, outlier_indices, axis=0)
    y_train = np.delete(y_train, outlier_indices)

    # データの正規化
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()
    x_train_scaled = scaler_x.fit_transform(x_train)
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1))

    # 線形回帰モデルを作成
    model = build_linear_model(x_train_scaled, y_train_scaled)

    # テストデータを作成
    x_test = dataset[outliers[0], outliers[1], 2].reshape(-1, 1)
    x_test_scaled = scaler_x.transform(x_test)  # テストデータも同様にスケーリング

    # モデルを使って予測
    y_pred_scaled = model.predict(x_test_scaled)

    # 予測結果を元のスケールに戻す
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    # 予測結果を表示
    print("予測結果:", y_pred)

    # モデルのスコアを計算
    score = model.score(x_test_scaled, y_pred_scaled)
    print("Score:", score)
