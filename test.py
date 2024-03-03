def change_viewbox(svg_content, new_viewbox):
    # SVGの開始タグを検索
    start_tag_index = svg_content.find("<svg")

    if start_tag_index == -1:
        # <svg>タグが見つからない場合はエラーを表示
        print("Error: <svg> tag not found in the SVG content.")
        return None

    # <svg>タグの終了位置を検索
    end_tag_index = svg_content.find(">", start_tag_index)

    if end_tag_index == -1:
        # <svg>タグの終了位置が見つからない場合はエラーを表示
        print("Error: Unable to find the end of <svg> tag.")
        return None

    # <svg>タグの中のviewBox属性を置き換える
    viewBox_attr_index = svg_content.find("viewBox", start_tag_index, end_tag_index)

    if viewBox_attr_index == -1:
        # viewBox属性が見つからない場合は新しく追加する
        svg_content = svg_content[:end_tag_index] + f' viewBox="{new_viewbox}"' + svg_content[end_tag_index:]
    else:
        # viewBox属性が見つかった場合は値を置き換える
        start_value_index = svg_content.find('"', viewBox_attr_index) + 1
        end_value_index = svg_content.find('"', start_value_index)
        svg_content = svg_content[:start_value_index] + new_viewbox + svg_content[end_value_index:]

    return svg_content

def change_viewbox_in_svg_file(input_file, output_file, new_viewbox):
    # SVGファイルを読み込む
    with open(input_file, 'r') as file:
        svg_content = file.read()

    # viewBoxを変更する
    new_svg_content = change_viewbox(svg_content, new_viewbox)

    if new_svg_content is not None:
        # 変更後のSVGファイルを保存する
        with open(output_file, 'w') as file:
            file.write(new_svg_content)
        print(f'Success: viewBox in {input_file} changed and saved to {output_file}')
    else:
        print('Error: viewBox change unsuccessful.')

# テスト用のSVGファイルのパスと新しいviewBoxの値
input_svg_file = 'test.svg'
output_svg_file = 'output.svg'
new_viewbox_value = '0 0 200 200'

# viewBoxを変更して保存
change_viewbox_in_svg_file(input_svg_file, output_svg_file, new_viewbox_value)
