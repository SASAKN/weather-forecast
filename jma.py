import requests
from bs4 import BeautifulSoup #ダウンロードしてなかったらpipでできるからやってね。
import csv

place_codeA = [44] #都道府県コード
place_codeB = [47662] #地域コード
place_name = ["東京"]

# URLで年と月ごとの設定ができるので%sで指定した英数字を埋め込めるようにします。
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1"

#取ったデータをfloat型に変えるやつ。(データが取れなかったとき気象庁は"/"を埋め込んでいるから0に変える)
def str2float(str):
  try:
    return float(str)
  except:
    return 0.0

if __name__ == "__main__":
  #都市を網羅
  for place in place_name:
    #最終的にデータを集めるリスト
    All_list = [['年月日', '降水量', '気温_平均', '気温_最高', '気温_最低', '湿度_平均', '湿度_最小', '日照時間']]
    print(place)
    index = place_name.index(place)

    # for文で該当期間抽出
    for year in range(1924,2024):
      print(year)
      # その年の1月～12月の12回を網羅する。
      for month in range(1,13):
        #2つの都市コードと年と月を当てはめる。
        r = requests.get(base_url%(place_codeA[index], place_codeB[index], year, month))
        r.encoding = r.apparent_encoding

        # サイトごとスクレイピング
        soup = BeautifulSoup(r.text)
        # findAllで条件に一致するものをすべて抜き出す。
        # 今回の条件はtrタグでclassがmtxになっているもの。
        rows = soup.findAll('tr',class_='mtx')

        # 表の最初の1~4行目はカラム情報なのでスライスする。
        rows = rows[4:]

        # 1日〜最終日までの１行を取得
        for row in rows:
          # trのなかのtdをすべて抜き出す
          data = row.findAll('td')

          #１行の中には様々なデータがあるので全部取り出す。
          rowData = [] #初期化
          rowData.append(str(year) + "/" + str(month) + "/" + str(data[0].string))
          rowData.append(str2float(data[3].string))
          rowData.append(str2float(data[6].string))
          rowData.append(str2float(data[7].string))
          rowData.append(str2float(data[8].string))
          rowData.append(str2float(data[9].string))
          rowData.append(str2float(data[10].string))
          rowData.append(str2float(data[16].string))

          #次の行にデータを追加
          All_list.append(rowData)

    #都市ごとにファイルを生成(csvファイル形式。名前は都市名)
    with open(place + '.csv', 'w',encoding="utf_8_sig") as file: #文字化け防止
      writer = csv.writer(file, lineterminator='\n')
      writer.writerows(All_list)

