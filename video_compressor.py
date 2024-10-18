import subprocess
import os
from tqdm import tqdm
import json
import re

# Input and output file paths
input_file = "HomeSpruce.mp4"
output_file = "HomeSpruceNew4.mp4"
target_size_mb = 4  # Target size in MB

# Path to ffmpeg and ffprobe executables - replace these with your actual paths if needed
ffmpeg_path = "ffmpeg"
ffprobe_path = "ffprobe"

def get_video_info(file_path):
    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Extract duration and bitrate
        duration = float(data['format']['duration'])
        bitrate = int(data['format']['bit_rate'])
        
        # Extract video resolution
        video_stream = next(s for s in data['streams'] if s['codec_type'] == 'video')
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        
        return duration, bitrate, width, height
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing ffprobe output: {e}")
    except (KeyError, StopIteration) as e:
        print(f"Error extracting video information: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None, None, None, None

def calculate_target_bitrate(duration, target_size_mb):
    target_size_bits = target_size_mb * 8 * 1024 * 1024
    target_bitrate = int(target_size_bits / duration)
    return target_bitrate

def check_ffmpeg_ffprobe():
    for cmd in [ffmpeg_path, ffprobe_path]:
        try:
            subprocess.run([cmd, "-version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Error: {cmd} not found. Please make sure it's installed and accessible.")
            return False
    return True

if not check_ffmpeg_ffprobe():
    exit(1)

try:
    # Get video information
    duration, original_bitrate, width, height = get_video_info(input_file)
    if duration is None or original_bitrate is None:
        raise ValueError("Could not determine video duration or bitrate.")

    # Calculate target bitrate
    target_bitrate = calculate_target_bitrate(duration, target_size_mb)
    
    print(f"Video resolution: {width}x{height}")
    print(f"Original bitrate: {original_bitrate/1024:.2f} kbps")
    print(f"Target bitrate: {target_bitrate/1024:.2f} kbps")

    # Determine scaling
    target_height = min(720, height)
    scale_filter = f"scale=-2:{target_height}"

    # Construct the ffmpeg command
    command = [
        ffmpeg_path,
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", "slower",
        "-crf", "23",
        "-maxrate", f"{target_bitrate}",
        "-bufsize", f"{target_bitrate*2}",
        "-c:a", "aac",
        "-b:a", "64k",
        "-ac", "1",
        "-vf", scale_filter,
        "-f", "mp4",
        "-progress", "pipe:1",
        output_file
    ]

    # Run the ffmpeg command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    # Setup progress bar
    pbar = tqdm(total=100, unit="%", bar_format="{l_bar}{bar} [ time left: {remaining} ]")

    # Track progress
    for line in process.stdout:
        if "out_time=" in line:
            match = re.search(r"out_time=(\d{2}):(\d{2}):(\d{2})\.", line)
            if match:
                hours, minutes, seconds = map(int, match.groups())
                current_time = hours * 3600 + minutes * 60 + seconds
                progress = min(int(100 * current_time / duration), 100)
                pbar.n = progress
                pbar.refresh()

    pbar.close()
    process.wait()

    if process.returncode == 0:
        print("\nCompression completed successfully!")
        output_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Output file size: {output_size:.2f} MB")
    else:
        print(f"\nAn error occurred during compression. Return code: {process.returncode}")

except subprocess.CalledProcessError as e:
    print(f"An error occurred while running a subprocess command: {e}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")