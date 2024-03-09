import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization, Flatten, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# ダミーの海面気圧データ生成（適切なデータセットを使用することが推奨されます）
# ここでは、ランダムな気圧データを生成しています。
n_samples = 1000
n_seq = 5
n_features = 1

pressure_data = np.random.rand(n_samples, n_seq, n_features)

# データの正規化
scaler = MinMaxScaler()
pressure_data_normalized = scaler.fit_transform(pressure_data.reshape(-1, 1)).reshape(n_samples, n_seq, n_features)

# データの整形
x = pressure_data_normalized[:, :-1, :]
y = pressure_data_normalized[:, -1, :]

# データの分割
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# ConvLSTMモデルの構築
model = Sequential()

model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), input_shape=(None, n_seq, n_features, 1), padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), padding='same', return_sequences=True))
model.add(BatchNormalization())

model.add(ConvLSTM2D(filters=64, kernel_size=(3, 3), padding='same', return_sequences=False))
model.add(BatchNormalization())

model.add(Flatten())
model.add(Dense(units=1, activation='linear'))

model.compile(optimizer='adam', loss='mse')

# モデルの訓練
model.fit(x_train, y_train, epochs=10, batch_size=16, validation_data=(x_test, y_test))

# モデルの評価
loss = model.evaluate(x_test, y_test)
print(f'Test Loss: {loss}')
