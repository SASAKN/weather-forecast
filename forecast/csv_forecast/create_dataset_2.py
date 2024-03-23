import numpy as np
import pandas as pd
from tqdm import tqdm
import random

def average(num1, num2):
    return (num1 + num2) / 2

def fix_cloudiness(outliner_keys, target_array):
    for outliner_key in tqdm(outliner_keys[:100]):
        row_index, col_index = outliner_key[0], outliner_key[1]
        cloudiness = target_array[row_index, col_index, 2]

        if cloudiness > 10:
            for index in range(7):
                left_value = target_array[row_index, col_index - index, 2] if col_index - index >= 0 else None
                right_value = target_array[row_index, col_index + index, 2] if col_index + index < target_array.shape[1] else None

                if left_value is not None and right_value is not None and left_value <= 10 and right_value <= 10:
                    cloudiness = np.mean([left_value, right_value])
                    break
                elif left_value is not None and left_value <= 10:
                    cloudiness = left_value
                    break
                elif right_value is not None and right_value <= 10:
                    cloudiness = right_value
                    break
                elif cloudiness is not None and cloudiness > 10 and target_array[row_index, col_index - index, 8] <= 24:
                    weather_code = target_array[row_index, col_index - index, 8]
                    if weather_code == 1:
                        cloudiness = 1
                    elif weather_code == 2:
                        cloudiness = random.choice([2, 3, 4, 5, 6, 7, 8])
                    elif weather_code == 3:
                        cloudiness = random.choice([9, 10])
                    elif weather_code in [4, 12, 13, 14, 17, 24]:
                        cloudiness = 10
                    else:
                        cloudiness = np.mean(target_array[row_index, :, 2])
                    break
                else:
                    cloudiness = np.mean(target_array[row_index, :, 2])

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
    
    
