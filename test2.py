import re

text = """<area alt="宇都宮" coords="149,183,160,194" href="../index.php?prec_no=41&amp;block_no=47615&amp;year=&amp;month=&amp;day=&amp;view=" onmouseout="javascript:initPoint();" onmouseover="javascript:viewPoint('s','47615','宇都宮','ウツノミヤ','36','32.9','139','52.1','119.4','1','1','1','1','1','1','9999','99','99','','','','','');" shape="rect"/>"""

# 正規表現を使用して数字を抜き出す
match = re.search(r"javascript:viewPoint\('.*?','(\d+)',", text)

if match:
    second_argument = match.group(1)
    print(second_argument)
else:
    print("2番目の引数が見つかりませんでした。")

