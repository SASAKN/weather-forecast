import csv

def filter_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # ヘッダーを書き込む
        header = next(reader)
        writer.writerow(header)

        # 条件に合致する行を書き込む
        for row in reader:
            if len(row) >= 17 and row[2] == "官" and "気圧" not in row[15] and "気圧" not in row[16]:
                writer.writerow(row)
#いらないデータのカット
def combine_columns(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # ヘッダーを書き込む
        header = next(reader)
        new_header = [header[0], header[1], header[7], header[8], header[9], header[10]]
        writer.writerow(new_header)

        # 指定された列を結合して新しい行を書き込む
        for row in reader:
            new_row = [row[0], row[1], row[7], row[8], row[9], row[10]]
            writer.writerow(new_row)

# 使用例
input_file_path = 'ame_master.csv'
output_file_path = 'output_filtered.csv'
filter_csv(input_file_path, output_file_path)
combine_columns(input_file_path, output_file_path)