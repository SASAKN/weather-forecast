import xarray as xr
import numpy as np
import glob
from tqdm import tqdm

# ベースパス
base_path = "./surf_jra55"

# 使うファイルのパス
file_paths = [
    "./surf_jra55/merged_1958.nc",
    "./surf_jra55/merged_1959.nc"
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

def compare_shapes(datasets, variable_name):
    shapes = [dataset[variable_name].shape for dataset in datasets]
    first_shape = shapes[0]
    for shape in shapes:
        if shape != first_shape:
            return False
    return True

# メイン
if __name__ == "__main__":

    #データセットから不一致を見つける

    num_file = 0
    num_miss = 0
    num_match = 0

    for year in range(1958, 2019):
        datasets = from_path_to_datasets(find_target_nc_file(year))
        num_file = num_file + 1

        for var_name in datasets[0].variables:
            if compare_shapes(datasets, var_name):
                print(f'{var_name}のShapeは一致。')
                num_match = num_match + 1
            else:
                print(f'{var_name}のShapeは不一致')
                num_miss = num_miss + 1

    print(f'ファイル数 : {num_file}\n一致する属性の数 : {num_match}\n一致しない属性の数 : {num_miss}')
            


