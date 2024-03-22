import numpy as np
import pandas as pd

def fix_cloudiness_2(row_idx, col_idx, target_array, target_number):
    index = 0

    try:
        while True:
            if (col_idx - index) <= 0 and index <= target_number:
                if index == 0 and target_array[row_idx, col_idx, 2] <= 10:
                    break
                elif index != 0 and target_array[row_idx, (col_idx - index), 2] <= 10 and target_array[row_idx, (col_idx + index), 2] <= 10:
                    target_array[row_idx, col_idx, 2] = (target_array[row_idx, (col_idx - index), 2] + target_array[row_idx, (col_idx + index), 2]) / 2
                    break
                elif index > target_number:
                    break
            else:
                break
            index += 1
    except IndexError:
        pass

    # 修正された配列を返す
    return target_array

def fix_cloudiness(outliner_keys, target_array):
    for outliner_key in outliner_keys:
        #必要な情報の取得
        row_index, col_index = outliner_key[0], outliner_key[1]
        cloudiness = target_array[row_index, col_index, 2]

        #外れ値を修正
        if cloudiness > 10:
            start_row = max(0, row_index - 24)
            end_row = min(row_index + 24 + 1, target_array.shape[0])
            start_col = max(0, col_index - 24)
            end_col = min(col_index + 24 + 1, target_array.shape[1])

            sum_value = 0
            count = 0

            for i in range(start_row, end_row):
                for j in range(start_col, end_col):
                    if (i, j) != (row_index, col_index):
                        sum_value += target_array[i, j, 2]
                        count += 1
            
            average_value = sum_value / count
            target_array[row_index, col_index, 2] = average_value
        
    return target_array







if __name__ == "__main__":
    array = np.load('./npz_data/dataset.npz')['dataset']
    
    # STEP 1 雲量の補完

    #11以上は外れ値なので修正
    print('雲量(Cloud)を修正します。')
    outliner_cloud_index = np.argwhere(array[:, :, 2] > 10)
    outliner_cloud_number = len(outliner_cloud_index)
    print(outliner_cloud_number)


    # #外れ値を修正
    # for outliner_cloud_idx in outliner_cloud_index:
    #     row_idx, col_idx = outliner_cloud_idx[0], outliner_cloud_idx[1]
    #     fix_cloudiness(row_idx, col_idx, array, outliner_cloud_number)
    #     print(array[row_idx, col_idx, 2])
    fix_cloudiness(outliner_cloud_index, array)

    #新しく計算し直す
    outliner_cloud_index = np.argwhere(array[:, :, 2] > 10)
    outliner_cloud_number = len(outliner_cloud_index)
    print(outliner_cloud_number)
    
    
