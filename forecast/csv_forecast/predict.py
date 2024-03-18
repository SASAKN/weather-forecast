#汎用
import os
import glob
import numpy as np
import json
from tqdm import tqdm

#機械学習
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from sklearn.model_selection import train_test_split

if __name__ == "__main__":

    #2つのデータセットを読み込む
    data_array = np.load('./npz_data/dataset.npz')['dataset_1']
    block_array = np.load('./npz_data/block_list.npz')['block']

    #XとYのデータを指定

    #Xのデータを作成
    result_x = []
    for z in data_array: #気圧配置のデータ
        for y in z: #地域ごとのデータ
            for x in y: #時間ごとのデータ配列
                result_x = np.delete(x, 3, axis=1) #現地_気圧, 海面_気圧を削除
    x = result_x

    #トレーニングとテストデータの分割
    train_x, test_x, train_y, test_y = train_test_split(x, y, train_size=0.8)

