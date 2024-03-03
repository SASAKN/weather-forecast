#==================================================#
#                    Library                       #
#==================================================#

import requests
from bs4 import BeautifulSoup as bs
import csv
from pdf2image import convert_from_path
import cairosvg
import os
import glob
import subprocess

#==================================================#
#                    Variable                      #
#==================================================#

#アメダスや気象台の地上観測データの地域コードなど

prec_codes_1 = ['44'] #都道府県コード
block_codes_1 = ['47662'] #地域コード

# ラジオゾンデ観測の地域コードなど

block_codes_2 = ['47600'] #地域コード
hours_list_2 = [9, 21] #ラジオゾンデの時間

# ベースURL1  prec_no = 都道府県コード, block_no = 地域コード, year = 年, month = 月, day = 日
base_url_1 = "https://www.data.jma.go.jp/stats/etrn/view/hourly_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=%s&view="

# ベースURL2 year = 年, month = 月, day = 日, hour = 時 (9, 21, 3, 15), point = 地域コード
base_url_2 = "https://www.data.jma.go.jp/stats/etrn/upper/view/hourly_usp.php?year=%s&month=%s&day=%s&hour=%s&atm=&point=%s&view="

# ベースURL3 0 = 西暦(4桁) 1 = 西暦下2桁 2 = 月
base_url_3 = "https://www.data.jma.go.jp/fcd/yoho/data/hibiten/%s/%s%s.pdf"

#==================================================#
#                 Related functions                #
#==================================================#

#文字列を少数に変換
def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

#都道府県コードにある地域コードを出力
def prec2block(prec_no, input_file):
    result_array = []

    with open(input_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0 and row[0].strip() == str(prec_no):
                result_array.append(row[1].strip())
    return result_array

# 数字を二桁に変換
def add_zero_to_single_digit(number):
    if 0 <= number < 10:
        result = f'0{number}'
    else:
        result = str(number)
    
    return result

# 列を配列に変換
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

#天気を数値に変換 - 参照 https://www.data.jma.go.jp/obd/stats/data/mdrr/man/tenki_kigou.html
def weather2float(weather):
    if  weather == "快晴":
        return 1
    elif weather == "晴":
        return 2
    elif weather == "薄雲":
        return 3
    elif weather == "曇":
        return 4
    elif weather == "煙霧":
        return 5
    elif weather == "砂じん嵐":
        return 6
    elif weather == "高い地ふぶき":
        return 7
    elif weather == "霧":
        return 8
    elif weather == "霧雨":
        return 9
    elif weather == "しゅう雨または止み間のある雨":
        return 10
    elif weather == "降水":
        return 11
    elif weather == "雨":
        return 12
    elif weather == "みぞれ":
        return 13
    elif weather == "雪":
        return 14
    elif weather == "着氷性の雨":
        return 15
    elif weather == "着氷性の霧雨":
        return 16
    elif weather == "凍雨":
        return 17
    elif weather == "霧雪":
        return 18
    elif weather == "しゅう雪または止み間のある雪":
        return 19
    elif weather == "あられ":
        return 20
    elif weather == "ひょう":
        return 21
    elif weather == "もや":
        return 22
    elif weather == "細氷":
        return 23
    elif weather == "雷":
        return 24

#雲量を数値変換
def cloud2float(cloud):
    if "+" in str(cloud) == 1:
        return str2float(cloud) + 0.5
    elif "-" in str(cloud) == 1:
        return str2float(cloud) - 0.5
    else:
        return str2float(cloud)

#16方位を度に変換
def direction2degrees(direction):
    directions = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東", 
                  "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西"]
    if not direction in directions:
        return 0.0
    
    degrees_per_direction = 360 / 16
    direction_index = directions.index(direction)
    return direction_index * degrees_per_direction

#==================================================#
#                    Functions                     #
#==================================================#

# 気象台データをダウンロード
def download_data_1():
    for prec in prec_codes_1:

        #Header
        All_list_1 = [['年月日時', '気圧_現地', '気圧_海面', '降水量', '気温', '湿度', '風速', '風向', '降雪', '天気', '雲量']] #集計データ
        
        #Index
        index = prec_codes_1.index(prec)

        # Block Array
        block_codes_1 = prec2block(prec_codes_1[index], 'test.csv')
        for block in block_codes_1:
            index_2 = block_codes_1.index(block)
            for year in range(2023, 2024):
                for month in range(1, 13):
                    for date in range(1, 32):
                        #処理中の年月日を表示
                        print(str(year) + "/" + str(month) + "/" + str(date))

                        #URL作成
                        req = requests.get(base_url_1%(prec_codes_1[index], block_codes_1[index_2], year, month, date))
                        req.encoding = req.apparent_encoding

                        #スクレイピング
                        page = bs(req.text, 'html.parser')

                        #3番目からのデータを使う
                        tmp_rows = page.select('#tablefix1 .mtx')
                        rows = tmp_rows[2:26]

                        for row in rows: 
                            #表の中身を抜き出す
                            data = row.select('td')

                            # 必要なデータを集め、配列にまとめる 
                            row_data = [] #初期化
                            for index_3 in [0, 1, 2, 3, 4, 7, 8, 9, 12, 14, 15]:
                                if data[index_3].string == None:
                                    if index_3 == 14: #天気
                                        weather = data[index_3].find("img")
                                        if not weather == None:
                                            row_data.append(weather2float(str(weather.get("alt"))))
                                    else:
                                        row_data.append("")
                                elif data[index_3].string == '--':
                                    if index_3 == 3: #降水量
                                        row_data.append(str2float("0"))
                                    elif index_3 == 12: #降雪量
                                        row_data.append(str2float("0"))
                                    else:
                                        row_data.append("")
                                else:
                                    if index_3 == 0: #年月日時
                                        row_data.append(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(data[index_3].string)) #年月日時
                                    elif index_3 == 9: #風向
                                        row_data.append(direction2degrees(data[index_3].string))
                                    elif index_3 == 15: #雲量
                                        row_data.append(str(data[index_3].string))
                                    else:
                                        row_data.append(str2float(data[index_3].string)) # 気圧_現地, 気圧_海面, 降水量, 気温, 湿度, 風速, 降雪量

                            #行をまとめる
                            All_list_1.append(row_data)
            #地域ごとにCSVを作成
            with open(block + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(All_list_1)

# ラジオゾンデ観測のデータをダウンロード
def download_data_2():
    for place in block_codes_2:
        All_list_2 = [['年月日時', '気圧', '気温', '相対湿度(%)' ,'風速(m/s)', '風向(°)']] #集計データ
        index = block_codes_2.index(place)
        for year in range(2023, 2024):
            for month in range(1, 13):
                for date in range(1, 32):
                    for hour in hours_list_2:
                        #処理中の年月日時を表示
                        print(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(hour))

                        #URL作成
                        req = requests.get(base_url_2%(year, month, date, hour, block_codes_2[index]))
                        req.encoding = req.apparent_encoding
                        
                        #スクレイピング
                        page = bs(req.text, 'html.parser')

                        #表の2番目のものをデータとして使う
                        if not page.select('#tablefix1 .mtx') == []:
                            rows = page.select('#tablefix1 .mtx')[1] #TRを取得

                        #必要なデータを集め配列にまとめる
                        row_data = [] #初期化
                        data = rows.select('td')

                        if not data[0].string == "///":
                            row_data.append(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(hour)) #年月日時
                            row_data.append(str2float(data[0].string)) #気圧
                            row_data.append(str2float(data[2].string)) #気温
                            row_data.append(str2float(data[3].string)) #相対湿度
                            row_data.append(str2float(data[4].string)) #風速
                            row_data.append(str2float(data[5].string)) #風向

                        #まとめる
                        All_list_2.append(row_data)

        with open(place + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(All_list_2)

#過去の天気図をダウンロード
def download_data_weather_map():
    for year in range(2002, 2003):
        for year_2 in range(2, 3):
            for month in range(1, 13):
                #処理中の年月を表示
                print(str(year) + "/" + str(month) + "/")


                #URL作成
                req = requests.get(base_url_3%(year, add_zero_to_single_digit(year_2), add_zero_to_single_digit(month)))
                req.encoding = req.apparent_encoding

                if not req.status_code == 404:
                    #ファイルの名前を作成
                    file_name = os.path.basename(base_url_3%(year, add_zero_to_single_digit(year_2), add_zero_to_single_digit(month)))

                    #保存ディレクトリ
                    save_dir = './map/'

                    #パス生成
                    save_path = os.path.join(save_dir, file_name)

                    #PDFを保存
                    with open(save_path, 'wb') as file:
                        file.write(req.content)


# 天気図をSVGに変換する関数
def weather_map2svg():
    # 天気図のPDFファイルを調べる
    pdf_list = []
    for pdf in glob.glob('./map/*.pdf'):
        pdf_list.append(pdf)
    
    #そのPDFをひとつづつSVGに変換する
    for pdf_path in pdf_list:
        subprocess.run(["pdf2svg", pdf_path, f'{pdf_path}.svg'])
        os.remove(pdf_path)
                    
#==================================================#
#                     Main                         #
#==================================================#

if __name__ == "__main__":

    # #都道府県コードをまとめる
    # prec_codes_1 = list(set(column_to_array('test.csv', 0)))

    # #ダウンロード
    # download_data_1()

    download_data_weather_map()
    weather_map2svg()
