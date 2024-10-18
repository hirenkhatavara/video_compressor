# Video Compressor with Target File Size

This Python script provides a simple yet powerful way to compress video files using FFmpeg, allowing you to specify a target file size in megabytes (MB). The script automatically adjusts the video bitrate to achieve the desired file size while maintaining the best possible quality.

## Key Features

- **Compress videos to a specified target size in MB**
- Automatic bitrate calculation based on video duration and target size
- Progress bar to show compression status
- Adjustable quality settings
- Support for various input video formats

## Prerequisites

Before you can use this script, you need to have the following installed on your system:

- Python 3.6 or higher
- FFmpeg (including ffprobe)
- tqdm Python library

## Installation

### 1. Python and tqdm

1. Install Python 3.6 or higher from [python.org](https://www.python.org/downloads/).
2. Install the required Python library:

   ```
   pip install tqdm
   ```

### 2. FFmpeg

#### Windows:

1. Download the FFmpeg build from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows).
2. Extract the ZIP file to a location on your computer (e.g., `C:\ffmpeg`).
3. Add the FFmpeg `bin` folder to your system PATH:
   - Right-click on 'This PC' or 'My Computer' and select 'Properties'.
   - Click on 'Advanced system settings'.
   - Click on 'Environment Variables'.
   - Under 'System variables', find and select 'Path', then click 'Edit'.
   - Click 'New' and add the path to the FFmpeg `bin` folder (e.g., `C:\ffmpeg\bin`).
   - Click 'OK' to close all dialogs.

#### macOS:

Using Homebrew:
```
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):

```
sudo apt update
sudo apt install ffmpeg
```

### 3. Script Setup

1. Clone this repository or download the script file.
2. Open the script in a text editor and modify the following variables at the top of the file:

   ```python
   input_file = "path/to/your/input_video.mp4"
   output_file = "path/to/your/output_video.mp4"
   target_size_mb = 10  # Set your desired target size in MB
   ```

## Usage

Run the script:

```
python video_compressor.py
```

The script will display progress and information about the compression process. Once completed, it will show the final file size of the compressed video, which should be close to your specified target size.

## Customization

You can adjust the following parameters in the script to fine-tune the compression:

- `target_size_mb`: Set this to your desired output file size in megabytes.
- `crf`: Controls the quality-to-filesize ratio. Lower values mean better quality but larger file size. Range: 0-51, default is 23.
- `preset`: Controls the encoding speed and compression efficiency. Options include 'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'. Default is 'slower'.
- Audio bitrate and channels: Adjust `-b:a` and `-ac` parameters in the FFmpeg command to change audio quality and number of channels.

## Troubleshooting

### FFmpeg Not Found

If you encounter an error saying FFmpeg is not found:

1. Ensure FFmpeg is correctly installed.
2. Check if FFmpeg is in your system PATH:
   - Open a new command prompt or terminal window.
   - Type `ffmpeg -version` and press Enter.
   - If you see FFmpeg version information, it's correctly installed and in your PATH.
   - If you get a "command not found" error, FFmpeg is not in your PATH.

3. If FFmpeg is installed but not in your PATH:
   - Find the full path to the FFmpeg executable.
   - In the script, update the `ffmpeg_path` and `ffprobe_path` variables with the full paths:

     ```python
     ffmpeg_path = "C:/path/to/ffmpeg.exe"  # Use forward slashes
     ffprobe_path = "C:/path/to/ffprobe.exe"
     ```

### Other Common Issues

- **Permission denied**: Ensure you have the necessary permissions to read the input file and write to the output location.
- **Input file not found**: Double-check the path to your input video file.
- **Out of memory**: For very large files or low memory systems, you may need to adjust the `bufsize` parameter in the FFmpeg command.
- **Unsupported codec**: Ensure your input video is in a format supported by FFmpeg. You may need to install additional codecs.

If you continue to experience issues, please check the [FFmpeg documentation](https://ffmpeg.org/documentation.html) or open an issue in this repository.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/video-compressor/issues) if you want to contribute.

## Acknowledgements

This script uses FFmpeg, a powerful multimedia framework. Visit [FFmpeg.org](https://ffmpeg.org/) for more information.