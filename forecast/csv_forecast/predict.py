#汎用
import os
import glob
import numpy as np
import json
from tqdm import tqdm

#機械学習
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM

#変数
region_codes = []
region_data = []

#関数

def extract_filename(file_path):
    file_name = os.path.basename(file_path)
    
    file_name_without_extension, _ = os.path.splitext(file_name)
    
    return file_name_without_extension

def find_target_csv_files():
    csvs = glob.glob("../data_utils/*.csv")

    #地点などのファイルを除外
    csvs.remove('../data_utils/ame_master.csv')
    csvs.remove('../data_utils/amedas.csv')
    csvs.remove('../data_utils/kousou_master.csv')

    return csvs

def load_np_arrays_from_npz(npz_file):
    return np.load(npz_file, allow_pickle=True)

def find_target_array_from_file(arrays, keyword):
    return arrays[str(keyword)]

if __name__ == "__main__":
    #メッセージを表示
    print(f'Weather Predictor Alpha v0.1')

    #ファイルの読み込み
    region_codes = (load_np_arrays_from_npz('./npz_data/block_list.npz'))['block']
    npz_file = load_np_arrays_from_npz('./npz_data/weather_data.npz')

    #地域コードを一覧表示
    print(f'気象庁地域コード : {region_codes.tolist()}')

    #UNIX時間と対応があるデータを作成
    all_array = []

    #指数表記禁止
    np.set_printoptions(suppress=True)

    for array_key in tqdm(list(npz_file.keys())):
        array = npz_file[f'{array_key}'].tolist()
        all_array.append(array)
    
    print(all_array[0][0][0])





