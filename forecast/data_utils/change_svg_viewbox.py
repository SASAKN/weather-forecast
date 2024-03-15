#ViewBoxを変更する関数
def change_viewbox(svg_content, min_x, min_y, x, y):

    new_viewbox = f'{min_x} {min_y} {x} {y}'

    start_tag_index = svg_content.find("<svg")

    if start_tag_index == -1:
        print("Error: <svg> tag not found in the SVG content.")
        return None

    end_tag_index = svg_content.find(">", start_tag_index)

    if end_tag_index == -1:
        print("Error: Unable to find the end of <svg> tag.")
        return None

    viewBox_attr_index = svg_content.find("viewBox", start_tag_index, end_tag_index)

    if viewBox_attr_index == -1:
        svg_content = svg_content[:end_tag_index] + f' viewBox="{new_viewbox}"' + svg_content[end_tag_index:]
    else:
        start_value_index = svg_content.find('"', viewBox_attr_index) + 1
        end_value_index = svg_content.find('"', start_value_index)
        svg_content = svg_content[:start_value_index] + new_viewbox + svg_content[end_value_index:]

    return svg_content

#svgファイルをViewBoxを変更して保存
def change_viewbox_in_svg_file(input_file, output_file, min_x, min_y, x, y):
    with open(input_file, 'r') as file:
        svg_content = file.read()

    new_svg_content = change_viewbox(svg_content, min_x, min_y, x, y)

    if new_svg_content is not None:
        with open(output_file, 'w') as file:
            file.write(new_svg_content)
        print(f'Success: viewBox in {input_file} changed and saved to {output_file}')
    else:
        print('Error: viewBox change unsuccessful.')

input_svg_file = 'test.svg'
output_svg_file = 'output.svg'
new_viewbox_value = '0 0 200 200'

change_viewbox_in_svg_file(input_svg_file, output_svg_file, 183, 0, 113, 179)
