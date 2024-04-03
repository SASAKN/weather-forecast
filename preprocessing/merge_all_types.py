import xarray as xr
import numpy as np
import glob

# ベースパス
base_path = "../jra55/arch/jra55/isobaric_1.25d/surf/"

# 使うファイルのパス
file_paths = [
    "../jra55/arch/jra55/data/isobaric_1.25d/surf/DEPR/DEPR_fhg_1959.nc",
    "../jra55/arch/jra55/data/isobaric_1.25d/surf/PRMSL/PRMSL_msl_1959.nc"
]

# ファイルパスを検索する
def find_target_nc_file():
    return glob.glob(f'{str(base_path)}{str("**/*.nc")}')

# パスからデータセットを開く
def from_path_to_datasets(path_array):
    datasets = []
    for path in path_array:
        datasets.append(xr.open_dataset(path))
    return datasets

# メイン
if __name__ == "__main__":

# データセットを取り出す
    datasets = from_path_to_datasets(file_paths)

    # 共通の座標変数を取り除く
    common_vars = ['lon', 'lat', 'time']

    # 共通な変数を抜き出す
    common_data = []
    for dataset in datasets:
        common_data.append(dataset[common_vars])

    # 共通でない変数を抜き出す
    specific_data = []
    for dataset in datasets:
        specific_data.append(dataset.drop_vars(common_vars))

    # 共通の変数を統合
    merged_common = xr.merge(common_data)

    # 共通でない変数を統合
    merged_spec = xr.merge(specific_data)

    # 全てを統合
    final_dataset = merged_common.merge(merged_spec)

    # 保存
    final_dataset.to_netcdf('merged.nc')



