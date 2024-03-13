import numpy as np

def generate_random_np_array(shape):
    """
    ランダムなNP配列を生成する関数
    
    引数:
    shape -- 配列の形状 (タプル)
    
    返り値:
    random_np_array -- ランダムなNP配列
    """
    random_np_array = np.random.random(shape)
    return random_np_array

def save_np_arrays_to_npz(array1, array2, array3, filename):
    """
    3つのNP配列をNPZ形式で保存する関数
    
    引数:
    array1 -- 1つ目のNP配列
    array2 -- 2つ目のNP配列
    array3 -- 3つ目のNP配列
    filename -- 保存するファイル名
    
    返り値:
    なし
    """
    np.savez(filename, **{"47110" : array1, "47220" : array2, "47330" : array3})

def load_np_arrays_from_npz(filename):
    """
    NPZ形式のファイルからNP配列を読み込む関数
    
    引数:
    filename -- 読み込むファイル名
    
    返り値:
    arrays -- ファイルから読み込んだNP配列を格納した辞書
    """
    npz_file = np.load(filename)
    arrays = {key: npz_file[key] for key in npz_file.files}
    npz_file.close()
    return arrays   

if __name__ == "__main__":
    # array_1 = generate_random_np_array((3, 3))
    # array_2 = generate_random_np_array((3, 3))
    # array_3 = generate_random_np_array((3, 3))
    # save_np_arrays_to_npz(array_1, array_2, array_3, 'test.npz')
    loaded_arrays = load_np_arrays_from_npz("test.npz")
    print(loaded_arrays['47220'])


