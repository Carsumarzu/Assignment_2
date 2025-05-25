import os

def main():
    input_file = "input.mp4"
    triangle_img = "triangle.png"
    square_img = "square.png"
    circle_img = "circle.png"
    output_file = "overlay.mkv"

    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

    audio_codec_text_content = "Audio codec\\: E-AC-3"
    video_codec_text_content = "Video codec\\: H.264qsv"
    moving_codec_x_expression = "w-mod(t*(w+tw)/20\\,w+tw)"

    y_start_members = "h-th-150"
    line_spacing_members = 30
    members = [
        "Vu Duc Minh - 20233868",
        "Pham Danh Tuan Dung - 20233844",
        "Nguyen Minh Huy - 20233852",
        "Luu Tien Dat - 20233835",
        "Le Thi Thao - 20233877"
    ]

    members_drawtext_filters = []
    for i, member in enumerate(members):
        y_pos = f"{y_start_members}+{line_spacing_members*i}"
        members_drawtext_filters.append(
            f"drawtext=fontfile='{font_path}':text='{member}':fontcolor=yellow:fontsize=24:x=10:y={y_pos}"
        )

    codec_drawtext_filters = [
        f"drawtext=fontfile='{font_path}':text='{video_codec_text_content}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=10:box=1:boxcolor=black@0.5",
        f"drawtext=fontfile='{font_path}':text='{audio_codec_text_content}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=40:box=1:boxcolor=black@0.5"
    ]

    all_text_filters = codec_drawtext_filters + members_drawtext_filters
    text_filter_chain = ",".join(all_text_filters)

    # Scale lớn hơn
    filter_complex = (
        f"[1:v]scale=140:140[tri];"
        f"[2:v]scale=120:120[sq];"
        f"[3:v]scale=100:100[cir];"
        f"[0:v]{text_filter_chain}[tmp1];"

        # Triangle: x = 100 + 80*sin(2πt), y = 50 + 50*cos(2πt)
        f"[tmp1][tri]overlay=x='100+80*sin(2*PI*t)':y='50+50*cos(2*PI*t)'[tmp2];"

        # Square: x = main_w/2 + 100*sin(t), y = main_h/2 + 100*cos(1.5*t)
        f"[tmp2][sq]overlay=x='(main_w/2)+100*sin(t)':y='(main_h/2)+100*cos(1.5*t)'[tmp3];"

        # Circle: x = mod(t*100, main_w + overlay_w) - overlay_w, y = 300 + 50*sin(2πt)
        f"[tmp3][cir]overlay=x='mod(t*100, main_w+overlay_w)-overlay_w':y='300+50*sin(2*PI*t)'"

    )

    command = (
        f'ffmpeg -i "{input_file}" -i "{triangle_img}" -i "{square_img}" -i "{circle_img}" '
        f'-filter_complex "{filter_complex}" '
        f'-c:v h264_videotoolbox -b:v 1M -c:a eac3 -b:a 192k "{output_file}"'
    )

    print(f"\n⚙️  Đang thực hiện lệnh:\n{command}\n")
    result = os.system(command)

    if result == 0:
        print(f"✅ Video đã được xử lý và lưu tại: {output_file}")
    else:
        print(f"❌ Có lỗi xảy ra trong quá trình xử lý video (mã lỗi: {result}).")

if __name__ == "__main__":
    main()
