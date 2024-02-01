# 必要なライブラリのインポート
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# CSVファイルの読み込み
data = pd.read_csv('weather_data.csv')

# 日付列の変換
data['年月日'] = pd.to_datetime(data['年月日'])
data['日付数値'] = data['年月日'].apply(lambda x: x.timestamp())

# 特徴量とターゲットの選択
features = data.drop(['年月日', '気温_平均'], axis=1)  # 予測対象が気温_平均の場合
target = data['気温_平均']

# データの正規化
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

# モデルの構築
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)  # 出力層のユニット数は1（回帰タスク）
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='mean_squared_error')

# モデルのトレーニング
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# トレーニングの過程を可視化
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.show()

# 新しいデータの作成
last_date = data['年月日'].max()
next_date = last_date + pd.DateOffset(days=1)

# 学習時に使用したデータの列の順序を取得
feature_names = features.columns.tolist()

# 新しいデータを作成
last_date = data['年月日'].max()
next_date = last_date + pd.DateOffset(days=1)

# 学習時に使用したデータの列の順序を取得
feature_names = features.columns.tolist()

# 新しいデータを作成し、全ての特徴量に対して学習データの平均値を設定
new_data = pd.DataFrame({
    '年月日': [next_date],
    '降水量': features['降水量'].mean(),
    '気温_最高': features['気温_最高'].mean(),
    '気温_最低': features['気温_最低'].mean(),
    '湿度_平均': features['湿度_平均'].mean(),
    '湿度_最小': features['湿度_最小'].mean(),
    '日照時間': features['日照時間'].mean(),
    '日付数値': next_date.timestamp()
})

# 学習時に使用した特徴量の順序に従ってデータを再構築
new_data = new_data[feature_names]

# 新しいデータの正規化
new_data_scaled = scaler.transform(new_data)

# モデルを使用して予測
predicted_temperature = model.predict(new_data_scaled)

print(f'明日の平均気温の予測値: {predicted_temperature[0][0]}')


