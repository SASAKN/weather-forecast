#==================================================#
#                    Library                       #
#==================================================#

# AIを使った希少予測
import os

#データ処理
import numpy as np
import pandas as pd

#グラフ描画
import matplotlib.pyplot as plt

#時系列処理
from datetime import datetime as dt
from datetime import timedelta

#機械学習データの用意
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

#機械学習ライブラリー
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization, Conv2D

#==================================================#
#                    Variable                      #
#==================================================#

# 設定
n_seq = 5 #シーケンス
n_features = 8 #特徴量の数


#==================================================#
#                 Releated Functions               #
#==================================================#

#ファイル名を取得
def extract_filename(file_path):
    file_name = os.path.basename(file_path)
    
    file_name_without_extension, _ = os.path.splitext(file_name)
    
    return file_name_without_extension

#日付を季節に変換
def date2season(month, day):
    month, day = int(month), int(day)
    
    #データが範囲内であるかを確認
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return 4 # 不正な日付
    
    #月を確認 - 1, 2季節ごとに判定
    if month == 2: #春,冬
        if day >= 4:
            return 0 #春
        elif day < 4:
            return 3 #冬
    elif month in [3, 4]: #春
        return 0 #春
    elif month == 5: #春,夏
        if day >= 5:
            return 1 #夏
        elif day < 5:
            return 0 #春
    elif month in [6, 7]: #夏
        return 1 #夏
    elif month == 8: #夏,秋
        if day >= 8:
            return 2 #秋
        elif day < 8:
            return 1 #夏
    elif month in [9, 10]: #秋
        return 2 #秋
    elif month == 11: #秋,冬
        if day >= 7:
            return 3 #冬
        elif day < 7:
            return 2 #秋
    elif month in [12, 1]: #冬
        return 3
    else:
        return 4 #エラー
    
# 数字を二桁に変換
def add_zero_to_single_digit(number):
    if 0 <= int(number) < 10:
        result = f'0{number}'
    else:
        result = str(number)
    
    return result

#24時を0時に変換
def format_hour(hour):
    if str(hour) == '24':
        return '00'
    else:
        return str(hour) 

#CSVを読み込む
def load_csv(input_csv):
    #CSVを読み込む
    data = pd.read_csv(input_csv, dtype={'column_name': str}, low_memory=False)

    #CSVから日付を0埋め
    added_zero_dates = []
    season_data = []
    for date in data['年月日時'].values.tolist():
        #/で分けて0埋め
        date_parts = date.split('/')
        year = int(date_parts[0])
        month = add_zero_to_single_digit(date_parts[1])
        day = add_zero_to_single_digit(date_parts[2])
        hour = format_hour(add_zero_to_single_digit(date_parts[3]))
        minute = '00'

        #datetimeに変換
        #エラーの原因がわかった 2/30 2/31などは存在しない
        try: 
            datetime_str = np.datetime64(f'{year}-{month}-{day}T{hour}:00:00')
        except Exception:
            try:
                datetime_str = np.datetime64(f'{year}-{month}-{add_zero_to_single_digit(str(int(day) - 1))}T{hour}:00:00')
            except Exception:
                try:
                    datetime_str = np.datetime64(f'{year}-{month}-{add_zero_to_single_digit(str(int(day) - 2))}T{hour}:00:00')
                except Exception:
                    datetime_str = np.datetime64(f'{year}-{month}-{add_zero_to_single_digit(str(int(day) - 3))}T{hour}:00:00')

        #季節に変換
        season = date2season(date_parts[1], date_parts[2])

        #データの配列作成
        added_zero_dates.append({'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute, 'datetime': datetime_str})
        season_data.append({'season': season})

    #データを作成、統合
    df_added_zero = pd.DataFrame(added_zero_dates)
    df_season = pd.DataFrame(season_data)
    data_2 = pd.concat([df_added_zero, df_season, data], axis=1)

    return data_2

#特徴量を抽出
def drop_features(input_data):
    #特徴量を抽出したデータフレームを作成
    target = input_data['気圧_海面'] #海面気圧(目的変数)
    features_1 = input_data['気圧_現地'] #現地気圧(説明変数)
    features_2 = input_data['気温'] #気温(説明変数)
    features_3 = input_data['風速'] #風速(説明変数)
    features_4 = input_data['風向'] #風向(説明変数)
    features_5 = input_data['湿度'] #湿度(説明変数)
    features_6 = input_data['datetime'] #時刻データ(説明変数)
    features_7 = input_data['season']
    headers = ['現地気圧', '海面気圧', '気温', '風速', '風向', '湿度', 'datetime', 'season']
    tmp_df = pd.DataFrame(headers)
    tmp_df = pd.concat([target, features_1, features_2, features_3, features_4, features_5, features_6, features_7], axis=1)
    features = pd.DataFrame(tmp_df)
    return features

#欠陥値を埋める
def fill_lack_value(input_df):
    #欠陥値の補完
    result = pd.DataFrame()
    input_df.fillna(method="ffill", inplace=True)
    result = input_df
    return result

#欠陥値を調べる
def find_lack_value(input_data):
    return input_data.isnull().sum()

#データの正規化
def scale_features(features):
    features_array = features.drop(['datetime'], axis=1).to_numpy()
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features_array)
    return features_scaled

#モデル作成
def model(x_train, x_test, y_train, y_test):
    #モデル定義
    model = Sequential()

    print(train_x.shape, train_y.shape)

    #Conv LSTMレイヤーの追加
    model.add(ConvLSTM2D(filters=64, kernel_size=(1, 3), input_shape=(None, 128, 128, 128)))

    #必要に応じてレイヤーを追加する(現在作業中)

    #出力
    model.add(Conv2D(filters=1, kernel_size=(1, 1), activation='sigmoid'))

    #モデルのコンパイル

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    #モデル訓練
    model.fit(x_train, y_train, epochs=50, batch_size=32, validation_data=(x_test, y_test))

    #モデル評価
    val_loss = model.evacute(x_test, y_test)
    print(f'テストのロス :{val_loss}')

    #モデルから予測
    predictions = model.predict(x_test)
    print(predictions)
    


#トレーニング


#画像生成

#メイン
if __name__ == "__main__":
    #特徴量を抽出
    features = drop_features(load_csv('test.csv'))

    #欠陥値を表示
    print(find_lack_value(features))

    #欠陥値を補完
    fill_lack_value(features)

    #データの正規化　ー　ただし日時は、正規化を行わない
    scaled_features = scale_features(features)

    #学習データと予測データに分割 
    train_x, test_x, train_y, test_y = train_test_split(scaled_features, features['気圧_海面'], train_size=0.8)








    