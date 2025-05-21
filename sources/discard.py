import subprocess
import json
import os
import matplotlib.pyplot as plt
 
def get_video_info(input_file):
    command = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=codec_type,nb_frames,r_frame_rate,duration,sample_rate:format=duration',
        '-of', 'json', input_file
    ]
    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        media_info = json.loads(process.stdout)
 
        total_frames, frame_rate_val, audio_sample_rate = None, None, None
        for stream in media_info['streams']:
            if stream.get('codec_type') == 'video':
                frame_rate_str = stream.get('r_frame_rate', '0/1')
                num_fps, den_fps = map(int, frame_rate_str.split('/'))
                frame_rate_val = num_fps / den_fps if den_fps != 0 else None
                total_frames_str = stream.get('nb_frames')
                if total_frames_str and total_frames_str.isdigit():
                    total_frames = int(total_frames_str)
                else:
                    duration = float(stream.get('duration', 0))
                    total_frames = int(duration * frame_rate_val)
            elif stream.get('codec_type') == 'audio':
                sample_rate_str = stream.get('sample_rate')
                if sample_rate_str and sample_rate_str.isdigit():
                    audio_sample_rate = int(sample_rate_str)
        return total_frames, frame_rate_val, audio_sample_rate
    except Exception as e:
        print(f"Lỗi khi lấy thông tin video: {e}")
        return None, None, None
 
def drop_frames_from_mp4(input_mp4, output_mp4, drop_percentage, frame_rate_val):
    keep_rate = 1.0 - (drop_percentage / 100.0)
    if keep_rate <= 0.0:
        print(f"⚠️ Tỷ lệ giữ lại là 0%. Bỏ qua {drop_percentage}%.")
        return
    mod_value = max(1, int(1 / keep_rate))
    video_filter_string = f"select='not(mod(n\\,{mod_value}))',setpts=N/({frame_rate_val}*TB)"
    command = [
        'ffmpeg', '-y',
        '-i', input_mp4,
        '-vf', video_filter_string,
        '-c:v', 'h264_qsv',
        '-an',
        output_mp4
    ]
    print(f"🎬 Xuất video với {drop_percentage}% khung hình bị loại bỏ → {output_mp4}")
    subprocess.run(command)
 
def process_multiple_drop_rates(input_file_path, drop_percentages):
    if not os.path.exists(input_file_path) or not input_file_path.lower().endswith('.mp4'):
        print("❌ File đầu vào không hợp lệ hoặc không phải .mp4.")
        return []
    base_name, _ = os.path.splitext(input_file_path)
    total_frames, frame_rate_val, _ = get_video_info(input_file_path)
    if total_frames is None or frame_rate_val is None:
        print("❌ Không thể lấy thông tin video.")
        return []
    output_files = []
    for percent in drop_percentages:
        output_file_path = f"{base_name}_dropped_{percent}.mp4"
        drop_frames_from_mp4(input_file_path, output_file_path, percent, frame_rate_val)
        output_files.append((percent, output_file_path))
    return output_files
 
def compute_metrics(original, distorted, psnr_log, ssim_log):
    subprocess.run([
        "ffmpeg", "-i", original, "-i", distorted,
        "-lavfi", f"[0:v][1:v]psnr=stats_file={psnr_log};[0:v][1:v]ssim=stats_file={ssim_log}",
        "-f", "null", "-"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 
def parse_metric_log(log_file, metric="psnr"):
    frame_vals = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                if metric == "psnr" and "average:" in line:
                    val = float(line.split("average:")[1].split()[0])
                    frame_vals.append(val)
                elif metric == "ssim" and "All:" in line:
                    val = float(line.split("All:")[1].split()[0])
                    frame_vals.append(val)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file log: {log_file}")
    return frame_vals
 
def plot_metric(data_dict, title, ylabel):
    plt.figure(figsize=(12, 4))
    for label, values in data_dict.items():
        plt.plot(values, label=label)
    plt.title(title)
    plt.xlabel("Frame Index")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
 
def evaluate_quality_vs_original(input_file_path, output_files):
    base_name, _ = os.path.splitext(input_file_path)
    psnr_data, ssim_data = {}, {}
 
    for rate, distorted_file in output_files:
        psnr_log = f"{base_name}_psnr_{rate}.log"
        ssim_log = f"{base_name}_ssim_{rate}.log"
 
        compute_metrics(input_file_path, distorted_file, psnr_log, ssim_log)
 
        psnr_vals = parse_metric_log(psnr_log, "psnr")
        ssim_vals = parse_metric_log(ssim_log, "ssim")
 
        psnr_data[f"{rate}%"] = psnr_vals
        ssim_data[f"{rate}%"] = ssim_vals
 
    plot_metric(psnr_data, "PSNR Between Original and Dropped Versions", "PSNR (dB)")
    plot_metric(ssim_data, "SSIM Between Original and Dropped Versions", "SSIM")
 
if __name__ == "__main__":
    input_file = input("Nhập tên file .mp4 đầu vào (ví dụ: video.mp4): ").strip()
    drop_rates = [0, 10, 20, 40, 50]
    output_files = process_multiple_drop_rates(input_file, drop_rates)
    if output_files:
        evaluate_quality_vs_original(input_file, output_files)