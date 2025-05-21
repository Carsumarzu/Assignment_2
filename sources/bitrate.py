import os
import re
import matplotlib.pyplot as plt
 
# ⚙️ Cấu hình
bitrates = [200, 500, 1000, 1200, 1500]  # kbps
input_file = "input.mp4"  # Video gốc
video_codec = "h264_qsv"  # Dùng Intel QSV
 
# 📁 Tạo thư mục lưu kết quả
output_dir = "bitrate"
os.makedirs(output_dir, exist_ok=True)
 
# ================================
# 🔁 Encode & đo PSNR/SSIM
# ================================
for bitrate in bitrates:
    output_file = os.path.join(output_dir, f"{bitrate}k.mp4")
    psnr_log = os.path.join(output_dir, f"{bitrate}k_psnr.log")
    ssim_log = os.path.join(output_dir, f"{bitrate}k_ssim.log")
 
    print(f"\n🎬 === Bitrate: {bitrate} kbps ===")
 
    # 🧪 Encode
    encode_cmd = (
        f'ffmpeg -y -hwaccel qsv -i "{input_file}" '
        f'-c:v {video_codec} -b:v {bitrate}k -c:a aac -b:a 128k '
        f'"{output_file}"'
    )
    print(f"🚀 Encoding:\n{encode_cmd}")
    os.system(encode_cmd)
 
    # 🧪 PSNR
    psnr_cmd = (
        f'ffmpeg -i "{input_file}" -i "{output_file}" '
        f'-lavfi psnr="stats_file={psnr_log}" -f null -'
    )
    print(f"\n📏 Calculating PSNR:\n{psnr_cmd}")
    os.system(psnr_cmd)
 
    # 🧪 SSIM
    ssim_cmd = (
        f'ffmpeg -i "{input_file}" -i "{output_file}" '
        f'-lavfi ssim="stats_file={ssim_log}" -f null -'
    )
    print(f"\n📏 Calculating SSIM:\n{ssim_cmd}")
    os.system(ssim_cmd)
 
print("\n✅ Đã hoàn tất tất cả các bitrate. Log PSNR/SSIM nằm trong thư mục:", output_dir)
 
# ================================
# 📊 Vẽ biểu đồ PSNR & SSIM
# ================================
 
def parse_psnr_log(file_path):
    psnr_values = []
    with open(file_path, "r") as f:
        for line in f:
            match = re.search(r"psnr_avg:([\d.]+)", line)
            if match:
                psnr_values.append(float(match.group(1)))
    return psnr_values
 
def parse_ssim_log(file_path):
    ssim_values = []
    with open(file_path, "r") as f:
        for line in f:
            match = re.search(r"All:([\d.]+)", line)
            if match:
                ssim_values.append(float(match.group(1)))
    return ssim_values
 
# 📈 PSNR Plot
plt.figure(figsize=(14, 5))
for bitrate in bitrates:
    log_path = os.path.join(output_dir, f"{bitrate}k_psnr.log")
    if os.path.exists(log_path):
        psnr_data = parse_psnr_log(log_path)
        plt.plot(psnr_data, label=f"{bitrate}k")
plt.title("PSNR over Time (per frame)")
plt.xlabel("Frame")
plt.ylabel("PSNR (dB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
 
# 📈 SSIM Plot
plt.figure(figsize=(14, 5))
for bitrate in bitrates:
    log_path = os.path.join(output_dir, f"{bitrate}k_ssim.log")
    if os.path.exists(log_path):
        ssim_data = parse_ssim_log(log_path)
        plt.plot(ssim_data, label=f"{bitrate}k")
plt.title("SSIM over Time (per frame)")
plt.xlabel("Frame")
plt.ylabel("SSIM")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()