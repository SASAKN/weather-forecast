import xarray as xr

# NetCDFファイルのパスを指定します。
file_path = "../jra55/arch/jra55/data/isobaric_1.25d/surf/PRMSL/PRMSL_msl_1958.nc"

# データセットを読み込みます。
dataset = xr.open_dataset(file_path)

# データセット内の変数名を表示します。
print(dataset.variables)
