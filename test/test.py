import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# データセットの作成
def create_dataset(past_weather_images, current_weather_images):
    # ここでは、過去の天気図と現在の天気図を組み合わせてデータセットを作成する簡単な例を示します。
    # 実際には、画像の前処理やデータの拡張などを行う必要があります。
    combined_images = np.concatenate((past_weather_images, current_weather_images), axis=1)
    return combined_images

# モデルの定義
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 6)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(3, activation='softmax')  # 3クラス分類（晴れ、曇り、雨）を想定
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 学習の実行
def train_model(model, dataset, labels):
    # ここでは、ImageDataGeneratorを使用してデータの拡張を行います。
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # モデルの学習
    model.fit(datagen.flow(dataset, labels, batch_size=32),
              steps_per_epoch=len(dataset) / 32, epochs=50)

# 予測の実行
def predict_weather(model, weather_image):
    # 予測を実行し、結果を返します。
    prediction = model.predict(np.expand_dims(weather_image, axis=0))
    return prediction

if __name__ == "__main__" :
    # 過去の天気画像と現在の天気画像を読み込む
    past_weather_images = np.load('weather_images2.npy')
    current_weather_images = np.load('weather_images2.npy')
    
    # データセットの作成
    dataset = create_dataset(past_weather_images, current_weather_images)
    
    # ラベルの読み込み（ここでは仮のラベルを使用）
    labels = np.load('labels.npy')
    
    # モデルの作成
    model = create_model()
    
    # モデルの学習
    train_model(model, dataset, labels)
    
    # 新しい天気画像で予測
    new_weather_image = np.load('new_weather_image.npy')
    prediction = predict_weather(model, new_weather_image)
    
    # 予測結果の表示
    print("予測結果:", prediction)

