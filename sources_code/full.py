# final_streaming_sender_script.py
import os
import shlex # Có thể hữu ích nếu sau này bạn muốn xử lý tham số an toàn hơn

def generate_and_stream_video(
    input_file="input.mp4",
    triangle_img="triangle.png",
    square_img="square.png",
    circle_img="circle.png",
    font_path="C\\:/Windows/Fonts/arial.ttf", # Sử dụng đường dẫn Windows với escape
    video_codec_text="Video codec\\: H.264 via h264_qsv", # Escape dấu :
    audio_codec_text="Audio codec\\: E-AC-3", # Escape dấu :
    members_list=[
        "Vu Duc Minh - 20233868",
        "Pham Danh Tuan Dung - 20233844",
        "Nguyen Minh Huy - 20233852",
        "Luu Tien Dat - 20233835",
        "Le Thi Thao - 20233877"
    ],
    video_bitrate="1M", # Ví dụ: "500k", "1M", "2M"
    audio_bitrate="192k",
    # Đây là đích đến của luồng stream, ví dụ script packet_discarder.py
    # hoặc IP của Máy Nhận nếu stream trực tiếp không qua mất gói
    output_stream_url="udp://127.0.0.1:5000"
):
    """
    Xây dựng và thực thi lệnh FFMPEG để stream video với overlay,
    codec chỉ định, và các thông số bitrate.
    """

    print(f"ℹ️  Chuẩn bị stream video: {input_file}")
    print(f"ℹ️  Bitrate Video mục tiêu: {video_bitrate}")
    print(f"ℹ️  Stream đến: {output_stream_url}")

    # --- Xây dựng phần drawtext cho tên thành viên ---
    y_start_members = "h-th-150"
    line_spacing_members = 30
    members_drawtext_filters = []
    for i, member in enumerate(members_list):
        y_pos = f"{y_start_members}+{line_spacing_members*i}"
        # Đảm bảo escape dấu ' nếu có trong tên thành viên
        member_escaped = member.replace("'", "\\'")
        members_drawtext_filters.append(
            f"drawtext=fontfile='{font_path}':text='{member_escaped}':fontcolor=yellow:fontsize=24:x=10:y={y_pos}"
        )

    # --- Xây dựng phần drawtext cho thông tin codec ---
    moving_codec_x_expression = "w-mod(t*(w+tw)/20\\,w+tw)" # Escape dấu , cho hàm mod
    codec_drawtext_filters = [
        f"drawtext=fontfile='{font_path}':text='{video_codec_text}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=10:box=1:boxcolor=black@0.5",
        f"drawtext=fontfile='{font_path}':text='{audio_codec_text}':fontsize=20:fontcolor=white:x='{moving_codec_x_expression}':y=40:box=1:boxcolor=black@0.5"
    ]

    all_text_filters = codec_drawtext_filters + members_drawtext_filters
    text_filter_chain = ",".join(all_text_filters)

    # --- Xây dựng chuỗi filter_complex hoàn chỉnh ---
    # Các input hình ảnh sẽ được đánh số từ 1 (0 là video chính)
    filter_complex = (
        f"[1:v]scale=100:100[tri];"
        f"[2:v]scale=80:80[sq];"
        f"[3:v]scale=60:60[cir];"
        f"[0:v]{text_filter_chain}[tmp1];"  # Áp dụng text overlays
        f"[tmp1][tri]overlay=x='mod(t*100, main_w+overlay_w)-overlay_w':y='50+20*sin(2*PI*t)'[tmp2];"
        f"[tmp2][sq]overlay=x='main_w-(mod(t*120, main_w+overlay_w))':y='150+25*cos(2*PI*t)'[tmp3];"
        f"[tmp3][cir]overlay=x='mod(t*80, main_w+overlay_w)-overlay_w':y='250+15*sin(2*PI*t+PI/2)'"
    )

    # --- Tính toán maxrate và bufsize ---
    try:
        if video_bitrate.upper().endswith('K'):
            vb_kbps = int(video_bitrate[:-1])
        elif video_bitrate.upper().endswith('M'):
            vb_kbps = int(video_bitrate[:-1]) * 1000
        else:
            # Nếu không có K hoặc M, giả sử người dùng nhập thẳng giá trị kbps
            vb_kbps = int(video_bitrate)
    except ValueError:
        print(f"❌ Lỗi: Định dạng video_bitrate ('{video_bitrate}') không hợp lệ. Hãy dùng dạng như '1000k' hoặc '1M'.")
        return

    maxrate_video = f"{vb_kbps}k"
    bufsize_video = f"{vb_kbps * 2}k" # bufsize thường gấp đôi bitrate/maxrate

    # --- Xây dựng toàn bộ lệnh FFMPEG ---
    # Sử dụng dấu nháy kép cho các đường dẫn và chuỗi filter phức tạp
    # để os.system xử lý đúng trên Windows.
    command = (
        f'ffmpeg -re -i "{input_file}" -i "{triangle_img}" -i "{square_img}" -i "{circle_img}" '
        f'-filter_complex "{filter_complex}" '
        f'-c:v h264_qsv -b:v {video_bitrate} -maxrate {maxrate_video} -bufsize {bufsize_video} '
        f'-c:a eac3 -b:a {audio_bitrate} '
        f'-f mpegts "{output_stream_url}"'
    )

    print(f"\n⚙️  Đang thực hiện lệnh FFMPEG:\n{command}\n")

    # Thực thi lệnh
    try:
        result = os.system(command)
        if result == 0:
            print(f"✅ FFMPEG đã chạy và stream thành công (hoặc hoàn thành nếu output là file).")
        else:
            print(f"❌ Có lỗi xảy ra khi chạy FFMPEG (mã lỗi: {result}). Hãy kiểm tra lại lệnh và log lỗi (nếu có).")
    except Exception as e:
        print(f"❌ Lỗi thực thi lệnh FFMPEG: {e}")

if __name__ == "__main__":
    # --- CẤU HÌNH CHO THÍ NGHIỆM HIỆN TẠI ---
    # Người dùng sẽ thay đổi các giá trị này cho mỗi lần chạy thí nghiệm
    
    INPUT_VIDEO = "input.mp4" # Đảm bảo file này tồn tại trong cùng thư mục với script
    
    TRIANGLE_IMAGE = "triangle.png" # Đảm bảo các file hình ảnh này tồn tại
    SQUARE_IMAGE = "square.png"
    CIRCLE_IMAGE = "circle.png"
    
    # Đường dẫn font cho Windows, sử dụng cú pháp FFMPEG chấp nhận
    # (Dấu \ được escape thành \\ trong Python string, FFMPEG sẽ nhận được C\:/...)
    FONT_PATH_WINDOWS = "C\\:/Windows/Fonts/arial.ttf" 
    # Hoặc thử: FONT_PATH_WINDOWS = "C:/Windows/Fonts/arial.ttf"
    # Hoặc: FONT_PATH_WINDOWS = "C\\:\\Windows\\Fonts\\arial.ttf"
    # Bạn cần kiểm tra xem FFMPEG trên máy bạn chấp nhận cú pháp nào tốt nhất khi gọi từ Python

    VIDEO_BITRATE_TARGET = "2M" # Ví dụ: "500k", "1M", "2M" (sẽ thay đổi theo từng thí nghiệm)
    
    # Địa chỉ IP và cổng của script packet_discarder.py (CHẠY TRÊN CÙNG MÁY GỬI NÀY)
    OUTPUT_URL = "udp://127.0.0.1:5000" 
    
    print(f"--- CHUẨN BỊ STREAM VIDEO VỚI OVERLAY ---")
    print(f"Video đầu vào: {INPUT_VIDEO}")
    print(f"Bitrate Video: {VIDEO_BITRATE_TARGET}")
    print(f"Stream đến (script mất gói): {OUTPUT_URL}")
    print(f"----------------------------------------")

    # Gọi hàm chính để thực hiện
    generate_and_stream_video(
        input_file=INPUT_VIDEO,
        triangle_img=TRIANGLE_IMAGE,
        square_img=SQUARE_IMAGE,
        circle_img=CIRCLE_IMAGE,
        font_path=FONT_PATH_WINDOWS,
        video_bitrate=VIDEO_BITRATE_TARGET,
        output_stream_url=OUTPUT_URL
        # các tham số khác như audio_bitrate, members_list, codec_text sẽ dùng giá trị mặc định trong hàm
    )