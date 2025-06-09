# Project: Video Processing and Quality Analysis Pipeline

This project is a pipeline for processing video files, including adding overlays and simulating packet loss, and then analyzing the quality of the processed videos using PSNR and SSIM metrics.

## 1. Project Overview

The core functionality of this project is to take an input video, apply various transformations, and then evaluate the impact of these transformations on the video's quality. This is particularly useful for research and development in video compression, streaming, and network performance analysis.

The project appears to simulate a real-world scenario where a video might be transmitted over a network, potentially suffering from data loss, and then have graphical information overlaid on it. The resulting video's quality is then objectively measured against the original.

## 2. File Structure

Here is a breakdown of the key files and directories in this project:

```

├── sources_code
│   ├── overlay.py
│   ├── packet_discarder.py
│   ├── main.m
│   ├── full.py
│   ├── circle.png
│   ├── square.png
│   ├── input.mp4
│   └── triangle.png
├── output
│   ├── overlay.mkv
│   ├── result_1.ts
│   ├── result_2.ts
│   ├── ...
│   └── result_6.ts
├── psnr_ssim
│   ├── result1_psnr_ssim
│   ├── result2_psnr_ssim
│   ├── ...
│   └── result6_psnr_ssim
└── README.md
```

- **`input.mp4`**: The original source video file that the processing pipeline will use.
- **`sources_code/`**: This directory contains all the source code for the project.
    - **`overlay.py`**: A Python script responsible for adding a graphical overlay to the video. It likely uses one of the provided PNG images.
    - **`packet_discarder.py`**: A Python script designed to simulate the effect of packet loss on the video stream.
    - **`main.m` / `full.py`**: These scripts likely orchestrate the entire video processing and analysis workflow, calling the other scripts in sequence.
    - **`circle.png`, `square.png`, `triangle.png`**: Image files that are used by `overlay.py` to add graphical elements to the video.
- **`output/`**: This directory stores the processed video files.
    - **`overlay.mkv`**: The output of the `overlay.py` script.
    - **`result_*.ts`**: A series of transport stream video files, likely the final output after all processing, including packet loss simulation.
- **`psnr_ssim/`**: This directory contains the results of the video quality analysis. Each subdirectory corresponds to one of the `result_*.ts` files and holds the calculated PSNR and SSIM scores.

## 3. How it Works

The project pipeline likely follows these steps:

1.  **Overlay Addition**: The `overlay.py` script takes the `input.mp4` and adds one of the provided images (`circle.png`, `square.png`, or `triangle.png`) as an overlay. The result is saved, for instance, as `overlay.mkv`.

2.  **Packet Loss Simulation**: The `packet_discarder.py` script simulates network packet loss on a video file (likely the original `input.mp4` or the one with the overlay). This results in a series of `result_*.ts` files, each representing a different level or pattern of packet loss.

3.  **Video Quality Analysis**: For each of the `result_*.ts` files, a script (likely part of `main.m` or `full.py`) calculates the Peak Signal-to-Noise Ratio (PSNR) and the Structural Similarity Index (SSIM). These metrics are used to objectively compare the quality of the processed videos to the original `input.mp4`. The results are stored in the `psnr_ssim` directory.

## 4. Getting Started

### Prerequisites

To run this project, you will likely need the following installed:

-   Python 3.x
-   OpenCV for Python (`opencv-python`)
-   NumPy
-   FFmpeg (for video processing and quality metric calculations)
-   Potentially other Python libraries for specific tasks.

You can install the necessary Python libraries using pip:

```bash
pip install opencv-python numpy
```

### Running the Project

While the exact execution command is not specified, a central script like `full.py` or a Makefile would typically be used to run the entire pipeline. A possible execution flow might be:

```bash
python full.py
```

This would execute the various stages of the project: applying overlays, simulating packet loss, and calculating the quality metrics.

## 5. Interpreting the Results

The output of this project is a set of processed video files and their corresponding quality scores.

-   **PSNR (Peak Signal-to-Noise Ratio)**: This metric measures the ratio between the maximum possible power of a signal and the power of corrupting noise. Higher PSNR values generally indicate a higher quality video. The values are typically expressed in decibels (dB).

-   **SSIM (Structural Similarity Index)**: This metric assesses the perceived quality of a video by comparing its structural information with the original. The SSIM value ranges from -1 to 1, where 1 indicates perfect similarity.

By analyzing the PSNR and SSIM scores in the `psnr_ssim` directory, you can quantitatively determine the impact of the different processing steps (like the severity of packet loss) on the visual quality of the video.
