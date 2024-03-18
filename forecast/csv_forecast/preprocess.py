#データ処理
import os
import glob
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

    #CSVの行を削除する
    data = data.drop(data.index[215833:])

    #重複したものを削除
    data = data.drop_duplicates()

    #日付をUnix時間にして、季節と地点緯度の追加
    added_zero_dates = [] #UNIX時間
    season_data = [] #季節

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

    #雲量をFloatに変換
    new_cloud_array = [] #雲量をFloatにしたもの

    for cloud in data['雲量'].values.tolist():

        # +と-の処理
        if str(cloud) in "+":
            new_cloud = float(str2float(cloud) + 0.5)
        elif str(cloud) in "-":
            new_cloud = float(str2float(cloud) - 0.5)
        elif str(cloud) == None:
            new_cloud = str2float('0')
        else:
            new_cloud = str2float(str(cloud))

        #配列に追加
        new_cloud_array.append({"Cloud" : new_cloud})
    
    #DataFrameを作成
    df_cloud = pd.DataFrame(new_cloud_array)


    #全てのデータを結合
    data_2 = pd.concat([df_added_zero, df_season, df_cloud, data], axis=1)

    return data_2

def df2np_array(df):
    return df.to_numpy()

def delete_unnecessary_row(df, unnecessary_header_array):
    return df.drop(unnecessary_header_array, axis=1)

def fill_lack_value_df(df):
    result = pd.DataFrame()
    df.fillna(method="ffill", inplace=True)
    result = df
    return result

def fill_lack_value_np(np_array):
    masked_array = np.ma.masked_invalid(np_array)
    fixed = np.ma.fix_invalid(masked_array, fill_value=np.nan).filled()
    return fixed

def count_lack_value(df):
    return df.isnull().sum()

def save_np_array(file_name, arrays):
    """
    引数: file_name, **arrays
    **arrays = キーワードと配列の対応させた辞書データ
    Example ) **{'47110' : array_1} #必ず、地点番号と対応させること
    """

    np.savez_compressed(f'npz_data/{str(file_name)}', **arrays)

def scale_features(ndarray):
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(ndarray)
    return scaled_features

def find_target_csv_files():
    csvs = glob.glob("../data_utils/*.csv")

    #地点などのファイルを除外
    csvs.remove('../data_utils/ame_master.csv')
    csvs.remove('../data_utils/amedas.csv')
    csvs.remove('../data_utils/kousou_master.csv')

    return csvs

#メイン
if __name__ == "__main__":
    #対象となるCSVを調べる
    target_csv_files = find_target_csv_files()

    #地域の一覧の配列を作成
    block_array = []
    for target_csv in target_csv_files:
        block_array.append(extract_filename(target_csv))
    save_np_array('block_list', {'block' : np.array(block_array)})

    #辞書の初期化
    files_dict = {}

    for target_csv in target_csv_files:

        print(f'[ PROCESSING ]現在進行中のファイル: {target_csv}')

        #CSVのデータ型を見る
        print(pd.read_csv(target_csv).dtypes)

        #CSVを処理
        data_csv = load_csv(target_csv)

        #風をベクトルに変換
        data_csv = wind2vector(data_csv)

        #CSVを表示
        pd.options.display.max_columns = 20
        print(data_csv.head())

        #必要のないデータをCSVから削除
        data_csv = delete_unnecessary_row(data_csv, ['年月日時', '雲量', '降雪'])

        #CSVのデータ型を見る
        print(data_csv.dtypes)

        #欠陥値の合計を出力
        print(count_lack_value(data_csv))

        #欠陥値を修正
        for i in [0, 1, 2]:
            data_csv = fill_lack_value_df(data_csv)

        #欠陥値の合計を再度出力
        print(count_lack_value(data_csv))

        #DataFrameをNumpy配列に変換
        data_np = df2np_array(data_csv)
        print(data_np)

        #Numpy配列の欠陥値を修正
        data_np = fill_lack_value_np(data_np)
        print(f'欠陥値: {np.sum(np.isnan(data_np), axis=0)}')

        #Shapeを確認
        print(data_np.shape)

        #辞書に追加
        files_dict[f'arr_{str(extract_filename(target_csv))}'] = data_np

    # train.npzとして保存
    save_np_array('weather_data', files_dict)