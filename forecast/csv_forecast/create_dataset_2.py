import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


# 線形回帰
def build_linear_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model

# ロジスティック回帰
def build_logistic_model(x, y):
    model = LogisticRegression(random_state=0)
    model.fit(x, y)
    return model

# ランダムフォレスト
def build_random_forest_model(x, y):
    model = RandomForestRegressor(random_state=0)
    model.fit(x, y)
    return model

if __name__ == "__main__":
    # データセットの読み込み
    dataset = np.load('./npz_data/dataset.npz')['dataset']

    # 外れ値のIndex, 正常値のIndex
    outliers = np.where(dataset[:, :, 2] > 10)
    inliers = np.where(dataset[:, :, 2] <= 10)

    # 外れ値と正常値の配列
    outliers_array = dataset[outliers[0], outliers[1], 2]
    inliers_array = dataset[inliers[0], inliers[1], 2]

    # データを作成


    

