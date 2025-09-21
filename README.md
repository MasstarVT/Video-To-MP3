# Video to MP3 Batch Converter

This Python program batch converts video files (e.g., MP4, MKV, AVI, MOV, WEBM, FLV) to MP3 audio files, preserving as much metadata as possible. It is designed for easy use and automation.

## Features
- Batch converts all videos in a folder (including subfolders) to MP3
- Preserves metadata (title, artist, album, year, genre, etc.) if available
- Skips files that have already been converted
- Uses FFmpeg for best results, falls back to MoviePy if needed
- Supports most common video formats

## Requirements
- Python 3.7+
- [FFmpeg](https://ffmpeg.org/download.html) (must be installed and in your PATH)
- Python packages: `moviepy`

## Installation
1. **Clone this repository:**
	```sh
	git clone https://github.com/MasstarVT/Video-To-MP3.git
	cd Video-To-MP3
	```
2. **Install Python dependencies:**
	```sh
	pip install moviepy
	```
3. **Install FFmpeg:**
	- Download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
	- Add FFmpeg to your system PATH (see [Windows guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/))

## Usage
1. Place your video files in the root folder or any subfolder (e.g., `Chrysanthemums/`).
2. Run the script:
	```sh
	python batch_video_to_mp3.py
	```
3. Converted MP3s will appear in the `completed/` folder, preserving the original folder structure.

### Custom Input/Output Folders
You can edit the script to change the input/output folders, or run with arguments (if you modify the script to accept them).

## Example
```
Video-To-MP3/
├── batch_video_to_mp3.py
├── Liked-Songs/
│   ├── 0001 - Example Video.mp4
│   └── ...
└── completed/
	 └── Liked Songs/
		  └── 0001 - Example Video.mp3
```

## Troubleshooting
- **moviepy not installed:** Run `pip install moviepy`.
- **FFmpeg not found:** Make sure FFmpeg is installed and in your PATH.
- **Permission errors:** Run your terminal as administrator or check folder permissions.

## License
MIT

---
*Created by MasstarVT*


