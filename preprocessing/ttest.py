import xarray as xr

# 統合するNetCDFファイルのパスを指定します。
file_paths = [
    "../jra55/arch/jra55/data/isobaric_1.25d/surf/DEPR/DEPR_fhg_1958.nc",
    "../jra55/arch/jra55/data/isobaric_1.25d/surf/PRMSL/PRMSL_msl_1958.nc"
]

# データセットを読み込みます。
datasets = [xr.open_dataset(path) for path in file_paths]

# 結合する変数を選択します。
common_vars = ['lon', 'lat', 'time']
specific_vars = ['DEPR_fhg', 'PRMSL_msl']

# 各データセットから共通の変数を選択して結合します。
merged_datasets = []
for ds in datasets:
    common_data = ds[common_vars]
    merged_datasets.append(common_data)

# 特定の変数が存在する場合は、それも選択して結合します。
for var in specific_vars:
    specific_data = []
    for ds in datasets:
        if var in ds.variables:
            specific_data.append(ds[var])
    if specific_data:
        merged_datasets.append(xr.merge(specific_data))

# 最終的なデータセットを結合します。
final_dataset = xr.merge(merged_datasets)

# 統合したデータセットを新しいNetCDFファイルとして保存します。
final_dataset.to_netcdf("merged_file.nc")
