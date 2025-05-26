% Xóa workspace và command window 
clear;
clc;
close all;

%% Cấu hình
video1_path = 'D:\Nén và mã hóa\ass2.1\input2.mp4';
video2_path = 'D:\Nén và mã hóa\ass2.1\result_6.ts';  % ✅ Đổi sang file .ts
output_dir = 'D:\Nén và mã hóa\ass2.1';
frame_interval = 1; % Khoảng cách lấy mẫu khung hình

%% Kiểm tra và tạo thư mục đầu ra
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

%% Khởi tạo VideoReader
try
    v1 = VideoReader(video1_path);
    v2 = VideoReader(video2_path);  % ✅ Đọc file .ts trực tiếp
catch ME
    error('Lỗi khi đọc video: %s', ME.message);
end

% Kiểm tra số khung hình hợp lệ
num_frames_to_process = min(floor(v1.Duration * v1.FrameRate), ...
                            floor(v2.Duration * v2.FrameRate));

%% Khởi tạo mảng kết quả
max_frames = floor(num_frames_to_process / frame_interval);
ssim_values = zeros(1, max_frames);
psnr_values = zeros(1, max_frames);
frame_indices = zeros(1, max_frames);
current_index = 0;

%% Tính SSIM và PSNR cho từng cặp khung hình
disp('Bắt đầu tính toán SSIM và PSNR...');
for i = 1:frame_interval:num_frames_to_process
    try
        frame1 = read(v1, i);
        frame2 = read(v2, i);

        if size(frame1, 3) == 3
            frame1_gray = rgb2gray(frame1);
        else
            frame1_gray = frame1;
        end
        if size(frame2, 3) == 3
            frame2_gray = rgb2gray(frame2);
        else
            frame2_gray = frame2;
        end

        if ~isequal(size(frame1_gray), size(frame2_gray))
            warning('Khung %d không khớp kích thước. Bỏ qua.', i);
            continue;
        end

        current_index = current_index + 1;
        ssim_values(current_index) = my_ssim(frame1_gray, frame2_gray);
        psnr_values(current_index) = my_psnr(frame1_gray, frame2_gray);
        frame_indices(current_index) = i;

        if mod(current_index, 10) == 0
            fprintf('Đã xử lý %d khung hình...\n', current_index);
        end

    catch ME
        warning('Lỗi tại khung %d: %s. Bỏ qua.', i, ME.message);
        continue;
    end
end

% Cắt kết quả thừa nếu có
ssim_values = ssim_values(1:current_index);
psnr_values = psnr_values(1:current_index);
frame_indices = frame_indices(1:current_index);

disp('Hoàn tất tính toán.');

%% Vẽ biểu đồ SSIM
figure;
plot(frame_indices, ssim_values, 'b', 'LineWidth', 1.5);
title('Biểu đồ SSIM theo khung hình');
xlabel('Số khung hình');
ylabel('Giá trị SSIM');
grid on;
ylim([0 1]);
saveas(gcf, fullfile(output_dir, 'ssim_plot_6.png'));

%% Vẽ biểu đồ PSNR
figure;
plot(frame_indices, psnr_values, 'r', 'LineWidth', 1.5);
title('Biểu đồ PSNR theo khung hình');
xlabel('Số khung hình');
ylabel('Giá trị PSNR (dB)');
grid on;
saveas(gcf, fullfile(output_dir, 'psnr_plot_6.png'));

%% Lưu dữ liệu
save(fullfile(output_dir, 'ssim_psnr_data.mat'), 'ssim_values', 'psnr_values', 'frame_indices');

disp(['Đã lưu biểu đồ và dữ liệu tại: ', output_dir]);

%% Hàm SSIM tự viết
function val = my_ssim(img1, img2)
    img1 = double(img1);
    img2 = double(img2);
    K1 = 0.01; K2 = 0.03; L = 255;
    C1 = (K1 * L)^2;
    C2 = (K2 * L)^2;

    mu1 = mean(img1(:));
    mu2 = mean(img2(:));
    sigma1 = std(img1(:));
    sigma2 = std(img2(:));
    sigma12 = mean((img1(:) - mu1) .* (img2(:) - mu2));

    val = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / ...
          ((mu1^2 + mu2^2 + C1) * (sigma1^2 + sigma2^2 + C2));
end

%% Hàm PSNR tự viết
function val = my_psnr(img1, img2)
    img1 = double(img1);
    img2 = double(img2);

    mse = mean((img1(:) - img2(:)).^2);
    if mse == 0
        val = Inf;
    else
        MAX_I = 255;
        val = 10 * log10((MAX_I^2) / mse);
    end
end
