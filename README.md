# forecast_weather

物理の先生に天気を予測したら、成績上げるよと言われたので、やる
その際に、使うデータは、JMAのデータです。
JMAのデータから気圧配置を予測し、等圧線を描きます。
その等圧線の数値配列から前線の位置を予測し、描き天気図を完成させます。

## Memo

観測所番号上2桁は、都道府県番号である
Ame_masterに載っている地域コードを信用してはいけない
天気図は、298x179のサイズでpdfにある
つまり、情報のサイズは、183
