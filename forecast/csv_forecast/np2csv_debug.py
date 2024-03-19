import numpy as np
from tqdm import tqdm

if __name__ == "__main__":
    all_array = []
    for array_key in list(np.load('./npz_data/weather_data.npz').keys()):
        array = np.load('./npz_data/weather_data.npz')[array_key]
        all_array.append(str(array.shape))
    # 出力ファイル名
    output_file = 'array_3d.txt'

    # 3次元配列をテキストファイルに書き込む
    with open(output_file, 'w') as f:
        for i in range(len(all_array)):
            for j in range(len(all_array[i])):
                line = ' '.join(map(str, all_array[i][j])) + ''
                f.write(line)
    
    
