import os
 
def main():

    input_file = "input.mp4"

    triangle_img = "triangle.png"

    square_img = "square.png"

    circle_img = "circle.png"

    bitrate_video_kbps = 800

    output_file = f"{bitrate_video_kbps}k_bitrate_with_shapes_animation_sine_cosine.mkv"
 
    # Đường dẫn font Arial trên Windows

    font_path = "C\\:/Windows/Fonts/arial.ttf"
 
    print(f"ℹ️  Sử dụng bitrate video mặc định: {bitrate_video_kbps}k")
 
    audio_codec_text_content = "Audio codec\\: E-AC-3"

    video_codec_text_content = "Video codec\\: H.264 via h264_qsv"

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
 
    # Scale 3 hình và overlay với chuyển động sin/cos

    filter_complex = (

        f"[1:v]scale=100:100[tri];"

        f"[2:v]scale=80:80[sq];"

        f"[3:v]scale=60:60[cir];"

        f"[0:v]{text_filter_chain}[tmp1];"

        f"[tmp1][tri]overlay=x='mod(t*100, main_w+overlay_w)-overlay_w':y='50+20*sin(2*PI*t)'[tmp2];"

        f"[tmp2][sq]overlay=x='main_w-(mod(t*120, main_w+overlay_w))':y='150+25*cos(2*PI*t)'[tmp3];"

        f"[tmp3][cir]overlay=x='mod(t*80, main_w+overlay_w)-overlay_w':y='250+15*sin(2*PI*t+PI/2)'"

    )
 
    command = (

        f'ffmpeg -i "{input_file}" -i "{triangle_img}" -i "{square_img}" -i "{circle_img}" '

        f'-filter_complex "{filter_complex}" '

        f'-b:v {bitrate_video_kbps}k -c:v h264_qsv -c:a eac3 -b:a 192k "{output_file}"'

    )
 
    print(f"\n⚙️  Đang thực hiện lệnh:\n{command}\n")

    result = os.system(command)
 
    if result == 0:

        print(f"✅ Video đã được xử lý và lưu tại: {output_file}")

    else:

        print(f"❌ Có lỗi xảy ra trong quá trình xử lý video (mã lỗi: {result}).")
 
if __name__ == "__main__":

    main()
 