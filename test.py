import requests
from bs4 import BeautifulSoup as bs
import csv
import os
import glob
import pandas as pd
import re

#気象台都道府県コードは、11から94
prec_codes = ['44']

# ブロックコードのクラス
class block_codes:
    def __init__(self, prec, block, block_code):
        self.prec = prec
        self.block = block
        self.block_code = block_code
    def get_csv_format(self):
        return [self.prec, self.block_code, self.block]

# クラスの配列
class_array = []

#ベースURL prec_no = 都道府県コード
base_url = "https://www.data.jma.go.jp/stats/etrn/select/prefecture.php?prec_no=%s"

# CSVから配列に変換
def column_to_array(input_file, column_index):
    result_array = []

    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile)

        #ヘッダー行のスキップ
        next(reader)

        # 指定した列を抽出して配列にまとめる
        for row in reader:
            if column_index < len(row):
                result_array.append(row[column_index])

    return result_array

#Tagをコードに変換
def tag2code(tag):
    match = re.search(r"javascript:viewPoint\('.*?','(\d+)',", str(tag))
    if match:
        arg = match.group(1)
        return arg
    else:
        return

#都道府県コードにある地域名を出力
def prec2block(prec_no, input_file):
    result_array = []

    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0 and row[0].strip() == str(prec_no):
                result_array.append(row[1].strip())
    return result_array

# CSV重複行削除
def delete_duplicates(input_file, output_file):
    # CSV読み込み
    result_csv = pd.read_csv(input_file, encoding='utf-8')

    #重複雨削除
    sorted_csv = result_csv.drop_duplicates(subset=["都道府県振興局番号", "観測所名"], keep='first', inplace=False)

    #ソート
    result_csv = sorted_csv.sort_values(by=["都道府県振興局番号"], ascending=True)

    #CSVに変換
    result_csv.to_csv(output_file, index=False)

#JMAからame_master.csvをダウンロードしなさい - https://www.jma.go.jp/jma/kishou/know/amedas/ame_master.zip

# 気象庁の観測地点コードは、5桁であるが、そのうち先頭2桁は、都道府県振興局番号である。
# そして、都道府県振興局番号は、スクレイピングに必要なものである。
def extract_first_two_digits_from_number(num):
    if isinstance(num, int) and 9999 < num < 100000:
        #スライス
        return int(str(num)[:2])
    else:
        return 0

#気圧を観測している地点のみにカットする
def filter_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # ヘッダーを書き込む
        header = next(reader)
        writer.writerow(header)

        # 条件に合致する行を書き込む
        for row in reader:
            if len(row) >= 17 and row[2] == "官" and "気圧" not in row[15] and "気圧" not in row[16]:
                writer.writerow(row)

# 観測地点一覧からいらないデータを削除
def combine_columns(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # ヘッダーを書き込む
        header = next(reader)
        new_header = ["都道府県振興局番号", header[3], header[7], header[8], header[9], header[10]]
        writer.writerow(new_header)

        # 指定された列を結合して新しい行を書き込む
        for row in reader:
            new_row = [str(extract_first_two_digits_from_number(int(row[1]))), row[3], row[7], row[8], row[9], row[10]]
            writer.writerow(new_row)

#観測地点のコードをダウンロード
def get_observation_points():
    for prec in prec_codes:
        #Indexを作成
        index = prec_codes.index(prec)

        #処理中の都道府県を表示
        print(f'処理中の都道府県振興局 : {prec_codes[index]}\n')

        #地域の配列を作成
        block_name = prec2block(prec_codes[index], 'filtered.csv')
        for block in block_name:
            #Indexを作成
            index_2 = block_name.index(block)

            #URLにアクセス
            req = requests.get(base_url%(prec_codes[index]))
            req.encoding = req.apparent_encoding

            #スクレイピング
            page = bs(req.text, 'html.parser')

            #要素を検索してみつける
            tmp_maps = page.find_all('map', {'name': 'point'})

            # エラーハンドリング
            if tmp_maps == []:
                print(f'[ INFO ]Prec None {prec_codes[index]}')
            else:      
                tmp_area = tmp_maps[0].find_all('area', {'alt': block_name[index_2]})
                if tmp_area == []:
                    print(f'[ INFO ]Block None {block_name[index_2]}')
                else:
                    #タグから地域コードを抜き出し、配列にクラスごと入れる
                    print(tag2code(tmp_area[0]))
                    class_array.append(block_codes(prec_codes[index], block_name[index_2], tag2code(tmp_area[0])))

#CSV書き込み
# def write_csv(output_file, data) {

# }


# 使用例
        
if __name__ == "__main__":
    #CSVの名前
    input_file_path = 'ame_master.csv'
    tmp_file_path = 'tmp_filtered.csv'
    tmp2_file_path = 'tmp_combine.csv'
    tmp3_file_path = 'filtered.csv'
    output_file_path = 'amedas.csv'

    #CSVから気圧を測っている地点を抜き出し
    filter_csv(input_file_path, tmp_file_path)
    #必要な情報のみをまとめ
    combine_columns(tmp_file_path, tmp2_file_path)
    #重複したものを削除
    delete_duplicates(tmp2_file_path ,tmp3_file_path)

    #都道府県コードをまとめる
    prec_codes = list(set(column_to_array(tmp3_file_path, 0)))

    #都道府県TO地域
    print(prec2block(11 ,tmp3_file_path))

    #地域コードをJMAからスクレイピング
    get_observation_points()

    print(f'{class_array[0].get_csv_format()}')
