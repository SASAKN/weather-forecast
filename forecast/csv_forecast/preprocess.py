#データ処理
import os
import sys
import numpy as np
import pandas as pd

#Sklearn
from sklearn.preprocessing import MinMaxScaler

#グラフ描画
import matplotlib.pyplot as plt

def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

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
        return 0
    else:
        return int(hour) 
    
#風力,風速をベクトルに変換
def wind2vector(df):
    wind_direction = df.pop('風向')
    wind_speed =  df.pop('風速')

    #風向をラジアンに変換
    wind_direction_radian = wind_direction * np.pi / 180

    # 風のXとYを計算
    df['wind_x'] = wind_speed * np.cos(wind_direction_radian)
    df['wind_y'] = wind_speed * np.sin(wind_direction_radian)

    return df


#CSVを読み込み、修正
def load_csv(input_csv):
    #CSVを読み込む
    data = pd.read_csv(input_csv, dtype={'column_name': str}, low_memory=False)

    #日付のゼロ埋めや、修正
    added_zero_dates = []
    season_data = []
    for date in data['年月日時'].values.tolist():
        #全て整数に変換
        date_parts = date.split('/')
        year, month, day, hour = map(int, date_parts[:4])

        #24時を0時
        hour = format_hour(str(hour))

        #datetimeに変換
        for day_offset in [0, 1, 2, 3]:
            try:
                adjusted_day = add_zero_to_single_digit(str(int(day) - day_offset))
                datetime_str = np.datetime64(f'{year}-{month:02d}-{adjusted_day}T{hour:02d}:00:00')
            except Exception:
                pass
        
        #Unix Time Stampに変換
        unix_time_stamp = datetime_str.astype('datetime64[s]').astype(int)
            

        #季節に変換
        season = str2float(str(date2season(month, day)))

        #データ配列作成
        added_zero_dates.append({'unix_time_stamp': unix_time_stamp})
        season_data.append({'season': season})

    #DataFrameを作成
    df_added_zero = pd.DataFrame(added_zero_dates)
    df_season = pd.DataFrame(season_data)

    #全てのデータを結合
    data_2 = pd.concat([df_added_zero, df_season, data], axis=1)

    return data_2

def df2np_array(df):
    return df.to_numpy()

def delete_unnecessary_row(df, unnecessary_header_array):
    return df.drop(unnecessary_header_array, axis=1)

def fill_lack_value(df):
    result = pd.DataFrame()
    df.fillna(method="ffill", inplace=True)
    result = df
    return result

def count_lack_value(df):
    return df.isnull().sum()

def save_np_array(np_array, file_name):
    np.savez_compressed(f'npz_data/{str(file_name)}', np_array)

def scale_features(ndarray):
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(ndarray)
    return scaled_features


#メイン
if __name__ == "__main__":
    #CSVのデータ型を見る
    print(pd.read_csv('test.csv').dtypes)

    #CSVを表示
    pd.options.display.max_columns = 20
    data_csv = load_csv('test.csv')

    #風をベクトルに変換
    data_csv = wind2vector(data_csv)
    print(data_csv.head())

    #必要のないデータをCSVから削除
    data_csv = delete_unnecessary_row(data_csv, ['年月日時', '降水量', '降雪', '雲量', '天気'])

    #CSVのデータ型を見る
    print(data_csv.dtypes)

    #欠陥値の合計を出力
    print(count_lack_value(data_csv))

    #欠陥値を修正
    for i in [0, 1]:
        data_csv = fill_lack_value(data_csv)

    #欠陥値の合計を再度出力
    print(count_lack_value(data_csv))

    #DataFrameをNumpy配列に変換
    np.set_printoptions(threshold=np.inf)
    data_np = df2np_array(data_csv)
    print(data_np)

    #データの正規化
    data_np = scale_features(data_np)

    #Shapeを確認
    print(data_np.shape)

    #npzとして保存
    save_np_array(data_np, 'test')












    
