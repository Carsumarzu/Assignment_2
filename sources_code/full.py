import os

def generate_and_stream_video(
    input_file="input.mp4",
    triangle_img="triangle.png",
    square_img="square.png",
    circle_img="circle.png",
    font_path="C\\:/Windows/Fonts/arial.ttf",
    video_codec_text="Video codec\\: H.264 via h264_qsv",
    audio_codec_text="Audio codec\\: E-AC-3",
    members_list=[
        "Vu Duc Minh - 20233868",
        "Pham Danh Tuan Dung - 20233844",
        "Nguyen Minh Huy - 20233852",
        "Luu Tien Dat - 20233835",
        "Le Thi Thao - 20233877"
    ],
    video_bitrate="1M",
    audio_bitrate="192k",
    output_stream_url="udp://<IP_MAY_TRUNG_GIAN>:5000" # Sẽ được thay thế ở dưới
):
    print(f"ℹ️  Chuẩn bị stream video: {input_file}")
    print(f"ℹ️  Bitrate Video mục tiêu: {video_bitrate}")
    print(f"ℹ️  Stream đến: {output_stream_url}")

    y_start_members = "h-th-150"
    line_spacing_members = 30
    members_drawtext_filters = []
    for i, member in enumerate(members_list):
        y_pos = f"{y_start_members}+{line_spacing_members*i}"
        member_escaped = member.replace("'", "\\'")
        members_drawtext_filters.append(
            f"drawtext=fontfile='{font_path}':text='{member_escaped}':fontcolor=yellow:fontsize=24:x=10:y={y_pos}"
        )

    moving_codec_x_expression = "w-mod(t*(w+tw)/20\\,w+tw)"
    codec_drawtext_filters = [
        f"drawtext=fontfile='{font_path}':text='{video_codec_text}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=10:box=1:boxcolor=black@0.5",
        f"drawtext=fontfile='{font_path}':text='{audio_codec_text}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=40:box=1:boxcolor=black@0.5"
    ]

    all_text_filters = codec_drawtext_filters + members_drawtext_filters
    text_filter_chain = ",".join(all_text_filters)

    filter_complex = (
        f"[1:v]scale=100:100[tri];"
        f"[2:v]scale=80:80[sq];"
        f"[3:v]scale=60:60[cir];"
        f"[0:v]{text_filter_chain}[tmp1];"
        f"[tmp1][tri]overlay=x='mod(t*100, main_w+overlay_w)-overlay_w':y='50+20*sin(2*PI*t)'[tmp2];"
        f"[tmp2][sq]overlay=x='main_w-(mod(t*120, main_w+overlay_w))':y='150+25*cos(2*PI*t)'[tmp3];"
        f"[tmp3][cir]overlay=x='mod(t*80, main_w+overlay_w)-overlay_w':y='250+15*sin(2*PI*t+PI/2)'"
    )

    try:
        if video_bitrate.upper().endswith('K'):
            vb_kbps = int(video_bitrate[:-1])
        elif video_bitrate.upper().endswith('M'):
            vb_kbps = int(video_bitrate[:-1]) * 1000
        else:
            vb_kbps = int(video_bitrate)
    except ValueError:
        print(f"❌ Lỗi: Định dạng video_bitrate ('{video_bitrate}') không hợp lệ.")
        return

    maxrate_video = f"{vb_kbps}k"
    bufsize_video = f"{vb_kbps * 2}k"

    command = (
        f'ffmpeg -re -i "{input_file}" -i "{triangle_img}" -i "{square_img}" -i "{circle_img}" '
        f'-filter_complex "{filter_complex}" '
        f'-c:v h264_qsv -b:v {video_bitrate} -maxrate {maxrate_video} -bufsize {bufsize_video} '
        f'-c:a eac3 -b:a {audio_bitrate} '
        f'-f mpegts "{output_stream_url}"'
    )

    print(f"\n⚙️  Đang thực hiện lệnh FFMPEG:\n{command}\n")

    try:
        result = os.system(command)
        if result == 0:
            print(f"✅ FFMPEG đã chạy và stream thành công.")
        else:
            print(f"❌ Có lỗi xảy ra khi chạy FFMPEG (mã lỗi: {result}).")
    except Exception as e:
        print(f"❌ Lỗi thực thi lệnh FFMPEG: {e}")

if __name__ == "__main__":
    
    INPUT_VIDEO = "input.mp4"
    TRIANGLE_IMAGE = "triangle.png"
    SQUARE_IMAGE = "square.png"
    CIRCLE_IMAGE = "circle.png"
    FONT_PATH_WINDOWS = "C\\:/Windows/Fonts/arial.ttf" 

    # THAY ĐỔI GIÁ TRỊ NÀY CHO MỖI KỊCH BẢN THÍ NGHIỆM
    VIDEO_BITRATE_TARGET = "1M"

    # THAY BẰNG ĐỊA CHỈ IP THẬT CỦA MÁY TRUNG GIAN
    IP_MAY_TRUNG_GIAN = "192.168.209.53" 
    OUTPUT_URL_TO_INTERMEDIATE_PC = f"udp://{IP_MAY_TRUNG_GIAN}:5000"

    print(f"--- CHUẨN BỊ STREAM VIDEO VỚI OVERLAY (3 MÁY) ---")
    print(f"Video đầu vào: {INPUT_VIDEO}")
    print(f"Bitrate Video: {VIDEO_BITRATE_TARGET}")
    print(f"Stream đến Máy Trung Gian (script mất gói): {OUTPUT_URL_TO_INTERMEDIATE_PC}")
    print(f"-------------------------------------------------")

    generate_and_stream_video(
        input_file=INPUT_VIDEO,
        triangle_img=TRIANGLE_IMAGE,
        square_img=SQUARE_IMAGE,
        circle_img=CIRCLE_IMAGE,
        font_path=FONT_PATH_WINDOWS,
        video_bitrate=VIDEO_BITRATE_TARGET,
        output_stream_url=OUTPUT_URL_TO_INTERMEDIATE_PC
    )