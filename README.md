# Social Video Downloader (All-in-One)

A powerful, desktop-based social media downloader built with Python. This tool is designed to provide high-quality video retrieval from Instagram and TikTok with advanced processing features like audio muting and quality enhancement.

## 🚀 Features

* **Multi-Platform Support:** Seamlessly download content from **Instagram** and **TikTok**.
* **Quality Enhancement (HD):** Native library-based enhancement to ensure the best possible resolution without relying on external AI APIs.
* **Audio Control:** Built-in functionality to **Mute Video** directly during the download process.
* **Flexible Downloading:** Supports both **Single Download** for quick saves and **Multiple Download** for batch processing.
* **Anti-Bot Protection:** Integrated **Custom Timer** to delay actions between downloads, significantly reducing the risk of being flagged or rate-limited as a bot.
* **Dynamic Storage:** Choose your preferred saving location via a file picker before the process starts.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Core Engine:** `yt-dlp` (Customized for high-speed retrieval)
* **Processing:** `FFmpeg` (for video-audio merging, muting, and enhancement)
* **Interface:** Python Standard GUI / Libraries

## 📂 Project Structure

To keep things lightweight and portable, this project is contained within a single optimized script:
`all_in_one_downloader_hd_mute.py`

## ⚙️ Installation & Usage

1. **Clone the repository:**
   `bash`
   git clone [https://github.com/UsernameAnda/Social-Video-Downloader.git](https://github.com/UsernameAnda/Social-Video-Downloader.git)
3. Install Dependencies:
Ensure you have FFmpeg installed on your system as it is required for the Mute and HD enhancement features. Then install the Python requirements:
`bash`
  pip install yt-dlp
4. Run the Application:
`bash`
  python all_in_one_downloader_hd_mute.py

Screenshot after compile:


<img width="647" height="823" alt="image" src="https://github.com/user-attachments/assets/f7e5b12b-83b9-481b-ac5f-113ac51c1921" />

