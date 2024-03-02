import re

text = "javascript:viewPoint('s','47678','八丈島','ハチジヨウ','33','07.3','139','46.7','151.2','1','1','1','1','1','1','9999','99','99','','','','','');"

# 正規表現を使用して数字を抜き出す
match = re.search(r"javascript:viewPoint\('.*?','(\d+)',", text)

if match:
    second_argument = match.group(1)
    print(second_argument)
else:
    print("2番目の引数が見つかりませんでした。")
