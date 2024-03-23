import numpy as np
from sklearn.linear_model import LinearRegression

# サンプルデータを生成（外れ値を含む）
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
y = np.array([2, 3, 4, 5, 6, 10, 8, 9, 12, 14])

# 外れ値を除いたデータを使用して線形回帰モデルを構築
regression_model = LinearRegression()
regression_model.fit(X[:-1], y[:-1])  # 最後のデータは外れ値として除外

# 外れ値を補完
outlier = np.array([X[-1]]).reshape(1, -1)
predicted_value = regression_model.predict(outlier)[0]

print("外れ値:", outlier)
print("補完値:", predicted_value)
