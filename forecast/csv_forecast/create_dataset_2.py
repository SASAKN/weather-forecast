import numpy as np
import pandas as pd

def fix_cloudiness(row_idx, col_idx, target_array, target_number):
    index = 0

    while True:
        try:
            if (col_idx - index) <= 0 and index <= target_number:
                if index == 0 and target_array[row_idx, col_idx, 2] <= 10:
                    break
                elif index != 0 and target_array[row_idx, (col_idx - index), 2] <= 10 and target_array[row_idx, (col_idx + index), 2] <= 10:  # 改変が必要である場合
                    target_array[row_idx, col_idx, 2] = (target_array[row_idx, (col_idx - index), 2] + target_array[row_idx, (col_idx + index), 2]) / 2
                    break
                elif index > target_number:
                    break
        except Exception:
            index += 1
            pass

        index += 1

    result_array = target_array
    return result_array




if __name__ == "__main__":
    array = np.load('./npz_data/dataset.npz')['dataset']
    
    # STEP 1 雲量の補完

    #11以上は外れ値なので修正
    print('雲量(Cloud)を修正します。')
    outliner_cloud_index = np.argwhere(array[:, :, 2] > 10)
    outliner_cloud_number = len(outliner_cloud_index)
    print(outliner_cloud_number)


    #外れ値を修正
    for outliner_cloud_idx in outliner_cloud_index:
        row_idx, col_idx = outliner_cloud_idx[0], outliner_cloud_idx[1]
        fix_cloudiness(row_idx, col_idx, array, outliner_cloud_number)
        print(array[row_idx, col_idx, 2])
