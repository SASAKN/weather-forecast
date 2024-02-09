import requests
from bs4 import BeautifulSoup as bs
import csv

# 地域コードの配列
place_code = [''] #湿度などのコード
place_code_2 = ['47646'] #気圧などのコード
place_name_2 = ["輪島"] #気圧などの名前
hours_list_2 = [9, 21, 3, 15] #気圧をとる時間

# ベースとなるURL
#year = 年, month = 月, day = 日, hour = 時 (9, 21, 3, 15), point = 地域コード
base_url = "https://www.data.jma.go.jp/stats/etrn/upper/view/hourly_usp.php?year=%s&month=%s&day=%s&hour=%s&atm=&point=%s&view="

def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

#tag2textの使い方
#index 0 気圧(hPa) index 2 高度(m) index 4 気温 index 6 相対湿度 index 8 風速(m/s) index 10 風向

def tag2text(data, index=0):
    try:
        return str(data).split('>')[index + 1].split('<')[0]
    except:
        return str('///')

# 気圧などを取得する関数
def download_data_2():
    for place in place_name_2:
        All_list = [['年月日', '気圧', '気温', '風速(m/s)', '風向(°)']] #集計データ
        index = place_name_2.index(place)

        for year in range(2023, 2024):
            print(year)

            for month in range(1, 13):
                for date in range(1, 32):
                    for hour in hours_list_2:

                        print(year,'/', month, '/', date, '/',hour)

                        #URL作成
                        req = requests.get(base_url%(year, month, date, hour, place_code_2[index]))
                        req.encoding = req.apparent_encoding
                        
                        #スクレイピング
                        page = bs(req.text, 'html.parser')

                        #表の2番目のものをデータとして使う
                        tmp_rows = page.select('#tablefix1 .mtx')[1]

                        #tdを検索(表の中身)
                        tmp_data = tmp_rows.select('td')

                        #中身が///は、なし
                        if not tag2text(tmp_data) == '///':
                            #中身を抜き出す
                            contents = tmp_data
                            print(tag2text(contents, 0))

                #コンテンツを表配列にまとめる
                for content in contents:
                    row_data = []
                    row_data.append(str(year) + "/" +  str(month) + "/" + str(date) + "/" + str(hour)) #年月日時を追加
                    row_data.append(str2float(tag2text(content, 0))) #気圧
                    row_data.append(str2float(tag2text(content, 4))) #気温
                    row_data.append(str2float(tag2text(content, 8))) #風速
                    row_data.append(str2float(tag2text(content, 10))) #風向

                    #表の内容を入れる
                    All_list.append(row_data)

        with open(place + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(All_list)

if __name__ == "__main__":
    download_data_2()





