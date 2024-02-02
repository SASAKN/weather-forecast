import requests
from bs4 import BeautifulSoup
import csv
import time  # Import time module for adding delays

def str2float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def scrape_weather_data(base_url, place_name, place_codeA, place_codeB):
    all_data = [['年月日', '降水量', '気温_平均', '気温_最高', '気温_最低', '湿度_平均', '湿度_最小', '日照時間']]

    for index, place in enumerate(place_name):
        print(f"Scraping data for {place}")
        for year in range(2023, 2024):
            print(f"Year: {year}")
            for month in range(1, 13):
                r = requests.get(base_url % (place_codeA[index], place_codeB[index], year, month))
                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.findAll('tr', class_='mtx')[4:]

                for row in rows:
                    data = row.findAll('td')
                    row_data = [
                        f"{year}/{month}/{data[0].string}",
                        str2float(data[3].string),
                        str2float(data[6].string),
                        str2float(data[7].string),
                        str2float(data[8].string),
                        str2float(data[9].string),
                        str2float(data[10].string),
                        str2float(data[16].string)
                    ]
                    all_data.append(row_data)

                time.sleep(1)  # Add a delay between requests to avoid overloading the server

        with open(f"{place}_weather_data.csv", 'w', encoding="utf_8_sig") as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(all_data)

if __name__ == "__main__":
    place_codeA = [44]
    place_codeB = [47662]
    place_name = ["東京"]
    base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=1&view=p1"

    scrape_weather_data(base_url, place_name, place_codeA, place_codeB)
