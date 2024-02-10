import requests
from bs4 import BeautifulSoup as bs
import csv

# 地域コードの配列
place_code = [''] #湿度などのコード
place_code_2 = ['47646'] #気圧などのコード
place_name_2 = ["輪島"] #気圧などの名前
hours_list_2 = [9, 21] #気圧をとる時間

# ベースとなるURL
#year = 年, month = 月, day = 日, hour = 時 (9, 21, 3, 15), point = 地域コード
base_url = "https://www.data.jma.go.jp/stats/etrn/upper/view/hourly_usp.php?year=%s&month=%s&day=%s&hour=%s&atm=&point=%s&view="

def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

# 気圧などを取得する関数
def download_data_2():
    for place in place_name_2:
        All_list = [['年月日', '気圧', '気温', '風速(m/s)', '風向(°)']] #集計データ
        index = place_name_2.index(place)

        for year in range(2023, 2024):
            for month in range(1, 13):
                for date in range(1, 32):
                    for hour in hours_list_2:
                        #処理中の年月日を表示
                        print(str(year) + "/" + str(month) + "/" + str(date) + "/" + str(hour))

                        #URL作成
                        req = requests.get(base_url%(year, month, date, hour, place_code_2[index]))
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
                        All_list.append(row_data)

    with open(place + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(All_list)

if __name__ == "__main__":
    download_data_2()





