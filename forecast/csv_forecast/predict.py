import os
import glob
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM

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
    return np.load(npz_file)

def find_target_array_from_file(arrays, keyword):
    return arrays[str(keyword)]

def build_model():
    #Modelを作成
    model = Sequential()
    model.add(LSTM(64, input_shape=(64, 64, 64)))

if __name__ == "__main__":
    csv_files = find_target_csv_files()
    npz_arrays = load_np_arrays_from_npz('npz_data/weatther_data.npz')
    #地点ごとに行う
    for tmp in csv_files:
        block_code = extract_filename(tmp)
        array = npz_arrays[f'{block_code}']
        


