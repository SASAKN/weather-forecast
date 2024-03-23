import numpy as np

# サンプルデータの作成
data = np.array([1, 2, 3, 4, 5, 100])

# 外れ値の定義（例えば、平均からの標準偏差が3倍以上のものを外れ値とする）
mean = np.mean(data)
std = np.std(data)
threshold = mean + 1.5 * std

# 外れ値を含む配列と含まない配列を作成
outliers = np.where(data > threshold)[0]
inliers = np.where(data <= threshold)[0]

# 外れ値を含む配列と含まない配列を表示
print("外れ値を含む配列:", data[outliers])
print("含まない配列:", data[inliers])
