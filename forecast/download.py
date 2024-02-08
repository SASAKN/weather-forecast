import requests
from bs4 import BeautifulSoup as bs
import csv

#気圧配置のデータが欲しいため、地域コードを複数用意
place_code = ['']

#気圧,風速,風向を学習
#year = 年, month = 月, day = 日, hour = 時 (9, 21, 3, 15), point = 地域コード
base_url = "https://www.data.jma.go.jp/stats/etrn/upper/view/hourly_usp.php?year=%s&month=%s&day=%s&hour=%s&atm=&point=%s&view="