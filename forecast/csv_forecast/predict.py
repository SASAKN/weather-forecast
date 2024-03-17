#汎用
import os
import glob
import numpy as np

#機械学習
from keras.models import Sequential
from keras.layers import LSTM

#変数
region_codes = []
region_data = []

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
    #ファイルの読み込み
    csv_files = find_target_csv_files()
    npz_file = load_np_arrays_from_npz('./npz_data/weather_data.npz')

    #地域コードの配列を作成
    for tmp in csv_files:
        region_codes.append(str(extract_filename(tmp)))

    print(region_codes)

    print(npz_file)


    
    




    
    




