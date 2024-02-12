import requests
from bs4 import BeautifulSoup as bs
import csv

#アメダスや気象台の地上観測データの地域コードなど

place_code_1_prec = ['44'] #都道府県コード
place_code_1_block = ['47662'] #地域コード
place_name_1 = ["東京"] #場所の名前

# ラジオゾンデ観測の地域コードなど

place_code_2 = ['47646', '47600'] #地域コード
place_name_2 = ["館野", "輪島"] #場所の名前
hours_list_2 = [9, 21] #ラジオゾンデの時間

# ベースURL1  prec_no = 都道府県コード, block_no = 地域コード, year = 年, month = 月, day = 日
base_url_1 = "https://www.data.jma.go.jp/stats/etrn/view/hourly_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=%s&view="

# ベースURL2 year = 年, month = 月, day = 日, hour = 時 (9, 21, 3, 15), point = 地域コード
base_url_2 = "https://www.data.jma.go.jp/stats/etrn/upper/view/hourly_usp.php?year=%s&month=%s&day=%s&hour=%s&atm=&point=%s&view="

#文字列を少数に変換
def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

#16方位をDegreesに変換
def direction2degrees(direction):
    directions = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東", 
                  "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西"]
    if not direction in directions:
        return 0.0
    
    degrees_per_direction = 360 / 16
    direction_index = directions.index(direction)
    return direction_index * degrees_per_direction

# 気象台データをダウンロード
def download_data_1():
    for place in place_name_1:
        All_list_1 = [['年月日時', '気圧_現地', '気圧_海面', '降水量', '気温', '湿度', '風速', '風向', '降雪', '天気', '雲量']] #集計データ
        index = place.index(place)
        for year in range(1984, 2024):
            for month in range(1, 13):
                for date in range(1, 32):
                    #処理中の年月日を表示
                    print(str(year) + "/" + str(month) + "/" + str(date))

                    #URL作成
                    req = requests.get(base_url_1%(place_code_1_prec[index], place_code_1_block[index], year, month, date))
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
                        row_data.append(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(data[0].string)) #年月日時
                        row_data.append(str2float(data[1].string)) #気圧_現地
                        row_data.append(str2float(data[2].string)) #気圧_海面

                        #降水量
                        if data[3].string == '--': #降水量がなければ
                            row_data.append(str2float("0")) #0mm
                        else : #降水があれば
                            row_data.append(str2float(data[3].string)) #降水量
                        
                        row_data.append(str2float(data[4].string)) #気温
                        row_data.append(str2float(data[7].string)) #湿度
                        row_data.append(str2float(data[8].string)) #風速
                        row_data.append(direction2degrees(data[9].string)) #風向
                        
                        #降雪量
                        if data[12].string == '--':
                            row_data.append(str2float("0")) #0mm
                        else : #降雪があれば
                            row_data.append(str2float(data[12].string)) #降雪量

                        #天気
                        weather = '' #初期化
                        if not data[14].find('img') == None:
                            weather = data[14].find('img')
                            row_data.append(str(weather.get('alt')))

                        #雲量
                        if not data[15].string == None:
                            row_data.append(str(data[15].string))
                        
                        #まとめる
                        All_list_1.append(row_data)
        with open(place + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(All_list_1)


# ラジオゾンデ観測のデータをダウンロード
def download_data_2():
    for place in place_name_2:
        All_list_2 = [['年月日時', '気圧', '気温', '風速(m/s)', '風向(°)']] #集計データ
        index = place.index(place)
        for year in range(2023, 2024):
            for month in range(1, 13):
                for date in range(1, 32):
                    for hour in hours_list_2:
                        #処理中の年月日時を表示
                        print(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(hour))

                        #URL作成
                        req = requests.get(base_url_2%(year, month, date, hour, place_code_2[index]))
                        req.encoding = req.apparent_encoding
                        
                        #スクレイピング
                        page = bs(req.text, 'html.parser')

                        #表の2番目のものをデータとして使う
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

if __name__ == "__main__":
    download_data_1()
    download_data_2()
