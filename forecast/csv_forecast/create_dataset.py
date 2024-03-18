#汎用
import os
import glob
import numpy as np
import json
from tqdm import tqdm
import csv

#変数
region_codes = []
region_data = []

#関数

def save_np_array(file_name, arrays):
    """
    引数: file_name, **arrays
    **arrays = キーワードと配列の対応させた辞書データ
    Example ) **{'47110' : array_1} #必ず、地点番号と対応させること
    """

    np.savez_compressed(f'npz_data/{str(file_name)}', **arrays)

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

def write_3d_array_to_csv(filename, data):
    """
    3次元配列をCSVファイルに書き込む関数。

    Parameters:
    - filename: 出力するCSVファイルのパス
    - data: CSVに書き込むデータを含む3次元リスト

    Returns:
    - None
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for matrix in data:
            for row in matrix:
                writer.writerow(row)
            # 3次元配列の各行の終わりに改行を追加
            csvfile.write("\n")

if __name__ == "__main__":
    #メッセージを表示
    print(f'Weather DataSet Creator Alpha v0.1')

    #STEP1 すべての配列をまとめて3次元配列にする

    #ファイルの読み込み
    region_codes = (load_np_arrays_from_npz('./npz_data/block_list.npz'))['block']
    npz_file = load_np_arrays_from_npz('./npz_data/weather_data.npz')

    #地域コードを一覧表示
    print(f'気象庁地域コード : {region_codes.tolist()}')

    #3次元配列
    all_array = []

    #指数表記禁止
    np.set_printoptions(suppress=True)

    #UNIX時間の重複を消して、3次元配列に変換
    for array_key in tqdm(list(npz_file.keys()), desc="Processing ...", miniters=1000):
        array = npz_file[f'{array_key}']
        unique_array = np.unique(array, axis=1)
        all_array.append(unique_array.tolist())

    #Numpy配列に変換し、保存。
    write_3d_array_to_csv('tmp.csv', all_array)
    save_array = np.array(all_array)
    save_np_array('dataset', {'dataset_1' : save_array})

    #メッセージを表示
    print(f'Finished : STEP1 !')
    







