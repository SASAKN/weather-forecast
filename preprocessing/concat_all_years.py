import xarray as xr
import numpy as np
import glob
from tqdm import tqdm

# ベースパス
base_path = "./jra55"

# 使うファイルのパス
file_paths = [
    "./jra55/merged_1958.nc",
    "./jra55/merged_1959.nc"
]

# 目的のファイルを探す
def find_target_nc_file(year):
    result = glob.glob(f'{base_path}/merged_{year}.nc')
    return result

# パスからデータセットを開く
def from_path_to_datasets(path_array):
    datasets = []
    for path in path_array:
        datasets.append(xr.open_dataset(path))
    return datasets

# メイン
if __name__ == "__main__":

    #データセットを取り出す
    datasets = from_path_to_datasets(file_paths)

    # 最初のデータセットを取り出す
    first_dataset = datasets[0]

    # 最初のデータセットから共通項目を抜き出す
    common_items = ['lon', 'lat']

    # 共通項目を抜き出す
    common_data = []
    for dataset in datasets:
        common_data.append(dataset[common_items])

    # データセットから時間を抜き出す
    time_data = []
    for dataset in datasets:
        time_data.append(dataset['time'])
    
    # データセットから気象変数を抜き出す
    weather_data = []
    for dataset in datasets:
        weather_data.append(dataset.drop_vars(['lon', 'lat', 'time']))
    
    # マージする
    merged_common_data = xr.merge(common_data)
    merged_weather_data = xr.merge(weather_data, compat='override')
    merged_dataset = xr.merge([merged_common_data, merged_weather_data])
    print(merged_dataset)

    




    





    # # 共通の内容である変数
    # common_values_vars = ['lon', 'lat']

    # # 共通の内容である変数を抜き出す
    # common_data = []
    # for dataset in datasets:
    #     common_data.append(dataset[common_values_vars])
    
    # # 'time'を処理する
    # time_data = []
    # for dataset in datasets:
    #     time_data.append(dataset['time'])
    
    # # 各気象変数についても処理する
    # specific_data = []
    # for dataset in datasets:
    #     specific_data.append(dataset.drop_vars(['lon', 'lat', 'time']))
    
    # # 共通な内容の変数を統合
    # merged_common = xr.merge(common_data)

    # # timeを統合
    # merged_time_data = xr.concat(time_data, dim='time')

    # # 気象変数を統合
    # merged_spec = xr.merge(specific_data, compat='override')

    # # 全てを統合
    # final_dataset = merged_common.merge(merged_time_data)
    # final_dataset = final_dataset.merge(merged_spec, compat='override')

    # # 保存
    # final_dataset.to_netcdf(f'./exp/merged.nc')


