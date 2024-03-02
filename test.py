import requests
from bs4 import BeautifulSoup as bs
import csv
import os
import glob
import pandas as pd

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




# 使用例
input_file_path = 'ame_master.csv'
tmp_file_path = 'tmp_filtered.csv'
tmp2_file_path = 'tmp_combine.csv'
tmp3_file_path = 'filtered.csv'
output_file_path = 'amedas.csv'
filter_csv(input_file_path, tmp_file_path)
combine_columns(tmp_file_path, tmp2_file_path)
delete_duplicates(tmp2_file_path ,tmp3_file_path)
prec_codes = column_to_array('filtered.csv', 0)

print(prec_codes)
