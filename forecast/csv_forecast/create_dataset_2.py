import numpy as np
import pandas as pd
from tqdm import tqdm
import random

def average(num1, num2):
    return (num1 + num2) / 2

def fix_cloudiness(outliner_keys, target_array):
    for outliner_key in tqdm(outliner_keys[:100]):  # 全ての外れ値キーに対してループする
        # 必要な情報の取得
        row_index, col_index = outliner_key[0], outliner_key[1]
        cloudiness = target_array[row_index, col_index, 2]

        # 外れ値を修正
        if cloudiness > 10:
            for index in range(7):
                if (target_array[row_index, col_index - index, 2] <= 10 and
                    target_array[row_index, col_index + index, 2] <= 10):
                    cloudiness = average(target_array[row_index, col_index - index, 2],
                                         target_array[row_index, col_index + index, 2])
                    break
                elif target_array[row_index, col_index - index, 2] <= 10:
                    cloudiness = target_array[row_index, col_index - index, 2]
                    break
                elif target_array[row_index, col_index + index, 2] <= 10:
                    cloudiness = target_array[row_index, col_index + index, 2]
                    break
                elif (target_array[row_index, col_index - index, 2] > 10 and
                      target_array[row_index, col_index - index, 8] <= 24):
                    weather_code = target_array[row_index, col_index - index, 8]
                    if weather_code == 1:
                        cloudiness = 1
                    elif weather_code == 2:
                        cloudiness = random.choice([2, 3, 4, 5, 6, 7, 8])
                    elif weather_code == 3:
                        cloudiness = random.choice([9, 10])
                    elif weather_code == 4 or weather_code == 12 or weather_code == 13 or weather_code == 14 or weather_code == 17 or weather_code == 24:
                        cloudiness = 10
                    break
                elif index == 6 and (target_array[row_index, col_index - index, 2] > 10 and
                                     target_array[row_index, col_index + index, 2] > 10):
                    cloudiness = np.mean(target_array[row_index, :, 2])
                elif index == 6:
                    cloudiness = np.mean(target_array[row_index, :, 2])
                else:
                    pass

        target_array[row_index, col_index, 2] = cloudiness

    return target_array




if __name__ == "__main__":
    array = np.load('./npz_data/dataset.npz')['dataset']
    
    # STEP 1 雲量の補完

    #外れ値の補完
    print('雲量(Cloud)を修正します。')
    
    #外れ値を調べる
    outliner_cloud_index = np.argwhere(array[:, :, 2] > 10)
    print(len(outliner_cloud_index))

    array = fix_cloudiness(outliner_cloud_index, array)

    #新しく計算し直す
    outliner_cloud_index = np.argwhere(array[:, :, 2] > 10)
    print(len(outliner_cloud_index))
    
    
