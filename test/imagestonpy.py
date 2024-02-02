import numpy as np
from PIL import Image
import glob

def png_images_to_npy(directory, filename):
    # PNG画像を読み込み、Numpy配列に変換して.npyファイルに保存する関数
    image_list = []
    for filepath in glob.glob(directory + '/*.png'):
        image = Image.open(filepath)
        image_array = np.array(image)
        image_list.append(image_array)
    images_array = np.array(image_list)
    np.save(filename, images_array)
    print(f"{filename}にPNG画像データを保存しました。")

if __name__ == "__main__":
    directory = "images/"  # PNG画像が保存されているディレクトリのパス
    filename = "weather_images.npy"
    png_images_to_npy(directory, filename)

