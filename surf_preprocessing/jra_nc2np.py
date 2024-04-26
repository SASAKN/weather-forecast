import glob
import os

import numpy as np
import xarray as xr
from tqdm import tqdm

# 入力ベースパス
nc_base_path = "./surf_jra55"

# 出力ベースパス
np_base_path = "./surf_data_np"

# 目的のファイルを探す
def find_target_nc_file(year):
    result = glob.glob(f'{nc_base_path}/merged_{year}.nc')
    return result

# パスからデータセットを開く
def from_path_to_datasets(path_array):
    datasets = []
    for path in path_array:
        datasets.append(xr.open_dataset(path))
    return datasets

# NetCDF4をNumpyに変換
def nc2np(dataset, part):
    # part = トレーニングデータかテストデータか
    # dataset = データセットのデータ

    dataset = xr.open_dataset(f'{nc_base_path}/merged_1959.nc')

    # ディレクトリを作成
    if part == "train":
        os.makedirs("./surf_data_np/train/", exist_ok=True)
    elif part == "test":
        os.makedirs("./surf_data_np/test", exist_ok=True)
    else:
        print(f'[ ERROR ! ]Unknown part : {part}')
        return
    
    # 属性ごとに配列に変換
    array_dict = {}
    for var in dataset.variables:

        # 共通データでなければ
        if var != 'lon' and var != 'lat':

            # Numpyに変換
            array = dataset[var].to_numpy()

            # 時間窓切り出し
            window_size = 4 # 時間ステップ
            time_windows_list = []

            # 時間窓を作成
            if var != 'time':
                for i in range(array.shape[0] - window_size + 1):
                    
                    # 時間窓配列を作成
                    time_window = array[i:i+window_size]

                    # 時間窓のリストを作成
                    time_windows_list.append(time_window)
            
            print(np.array(time_windows_list).shape)











            if var != 'time':
                print(array[0][0][0])
                print(array[0][0][1])
                print(array[0][0][2])
                print(array[0][0][3])

            # 辞書に追加
            array_dict.update({f'{str(var)}': array})

    # print(array_dict)


    


    

    

if __name__ == "__main__":

    # メッセージを表示
    print("Copyright SASAKEN 2024")


    # 年ごとに気象変数と時間を処理する
    for year in tqdm(range(1958, 1959), desc='Processing ...'):
        # データセットを読み込む
        datasets = from_path_to_datasets(find_target_nc_file(year))

        for dataset in datasets:

            # Numpy配列に変換する
            nc2np(dataset, "train")

        
    
            







