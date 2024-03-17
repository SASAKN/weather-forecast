import numpy as np

# 仮想的なデータの例として、各地点の気圧配置データが1時間ごとの2次元配列として与えられるとします
# data_point_A, data_point_B, data_point_C はそれぞれ地点A、地点B、地点Cの気圧配置データを表します
data_point_A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # 地点Aの気圧配置データ
data_point_B = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]  # 地点Bの気圧配置データ
data_point_C = [[19, 20, 21], [22, 23, 24], [25, 26, 27]]  # 地点Cの気圧配置データ

# 各地点のデータを横に連結して1つのデータセットに結合する
combined_data = np.stack([data_point_A, data_point_B, data_point_C]).T

print(combined_data)
