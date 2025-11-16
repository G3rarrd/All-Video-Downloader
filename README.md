
# AllVideoDownloader
**AllVideoDownloader** is a Python CLI tool that allows you to download videos and audio from multiple platforms like YouTube, TikTok, Instagram, and more. It supports format selection, automatic aspect ratio correction, and metadata extraction

![alt text]()

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech%20stack)
- [Quick Start](#quick%20start)
- [Installations](#installations)
- [Repository Structure](#repository%20structure)

## Features
- 🎬 Multi-platform support: YouTube, TikTok, Instagram, etc.
- ⚙️ Video format and audio stream analysis and combination.
- 📏 Automatic aspect ratio adjustment for vertical videos using FFmpeg.
- 📝 Metadata extraction: title, views, likes, duration, uploader if available.
- 🎯 Filename handling for long or special-character titles.

## Tech Stack
**Language:**
- Python 3.13

**Dependencies:**
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - for downloading videos and audio
- platformdirs - for locating the user's directories folder cross-platform 
- Python standard libraries: `pathlib`, `re`, `subprocess`,`json`,`collections`
**External Tools:**
- FFmpeg - for video post-processing

## Quick Start
> [!Note] Ensure you are in the same directory as the AllVideoDownloader class when creating and running this python file.

``` python
from all_video_downloader import AllVideoDownloader

# Initialize downloader with a video URL
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
downloader = AllVideoDownloader(video_url)

# Display available video + audio formats
downloader.display_video_audio_format_info()

# Download a specific format by ID (1-based)
downloader.download(1)

# Access full metadata as JSON
metadata = downloader.display_all_metadata()
print(metadata)

```
- Downloads automatically to your system **Downloads folder**
- And displays the downloaded vid information

**Alternative**
- Head to the src directory and type the below 
```bash
python main.py
```
- Gives you the freedom to download from any copied video URL and pick any video format
- Ensure your **virtual environment is activated** when doing the above

## Installations
### System Requirements
- Python 3.13+
- FFmpeg installed and available in your system PATH
- Operating System: Windows, maxOS, or Linux

### Clone the Repository
```bash
git clone https://github.com/G3rarrd/All-Video-Downloader.git
cd all_video_downloader
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### FFmpeg Setup
- Ensure **FFmpeg** is installed on your system and added to the PATH.
- Download it here: [FFmpeg.org](https://www.ffmpeg.org/download.html)
- Test installation
```bash
ffmpeg -version
```
## Repository Structure
```css
├── requirements.txt
├── readme.md
├── src
│   ├── all_video_downloader.py
│   ├── main.py
│   └── __pycache__
│       └── all_video_downloader.cpython-313.pyc
```

#