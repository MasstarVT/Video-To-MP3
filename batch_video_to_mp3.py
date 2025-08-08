import os
import sys
import subprocess

def check_dependencies():
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        # Check if ffmpeg is available
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except ImportError:
        print("The 'moviepy' library is not installed. Please install it with: pip install moviepy")
        sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg is not installed or not in PATH. Please install FFmpeg for better metadata preservation.")
        print("You can download it from: https://ffmpeg.org/download.html")
        sys.exit(1)

def extract_metadata_from_video(video_path):
    """Extract metadata from video file using ffprobe"""
    try:
        # Use ffprobe to get metadata with UTF-8 encoding
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_format', '-show_streams', video_path
        ], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        
        import json
        if result.stdout:
            data = json.loads(result.stdout)
            
            metadata = {}
            # Extract format metadata
            if 'format' in data and 'tags' in data['format']:
                tags = data['format']['tags']
                # Map common tags to ID3 equivalents (case-insensitive search)
                for key, value in tags.items():
                    key_lower = key.lower()
                    if key_lower in ['title']:
                        metadata['title'] = value
                    elif key_lower in ['artist', 'author']:
                        metadata['artist'] = value
                    elif key_lower in ['album']:
                        metadata['album'] = value
                    elif key_lower in ['date', 'year', 'creation_time']:
                        metadata['date'] = value[:4] if len(value) >= 4 else value  # Extract year
                    elif key_lower in ['genre']:
                        metadata['genre'] = value
                    elif key_lower in ['album_artist', 'albumartist']:
                        metadata['album_artist'] = value
                    elif key_lower in ['track']:
                        metadata['track'] = value
            
            return metadata
        else:
            return {}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return {}

def convert_with_ffmpeg(video_path, mp3_path, metadata=None):
    """Convert video to MP3 using ffmpeg with metadata preservation"""
    try:
        # Build ffmpeg command
        cmd = ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a']
        
        # Add metadata if available
        if metadata:
            for key, value in metadata.items():
                # Clean the value to avoid encoding issues
                clean_value = str(value).replace('"', '\\"')
                if key == 'title':
                    cmd.extend(['-metadata', f'title={clean_value}'])
                elif key == 'artist':
                    cmd.extend(['-metadata', f'artist={clean_value}'])
                elif key == 'album':
                    cmd.extend(['-metadata', f'album={clean_value}'])
                elif key == 'date':
                    cmd.extend(['-metadata', f'date={clean_value}'])
                elif key == 'genre':
                    cmd.extend(['-metadata', f'genre={clean_value}'])
                elif key == 'album_artist':
                    cmd.extend(['-metadata', f'album_artist={clean_value}'])
                elif key == 'track':
                    cmd.extend(['-metadata', f'track={clean_value}'])
        
        cmd.extend(['-y', mp3_path])  # -y to overwrite output file
        
        # Run ffmpeg with proper encoding
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, 
                              encoding='utf-8', errors='ignore')
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr if e.stderr else 'Unknown error'}")
        return False

def batch_convert_videos_to_mp3(input_folder, output_folder):
    from moviepy.video.io.VideoFileClip import VideoFileClip
    video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv']
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for dirpath, _, filenames in os.walk(input_folder):
        rel_path = os.path.relpath(dirpath, input_folder)
        out_dir = os.path.join(output_folder, rel_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in video_exts):
                video_path = os.path.join(dirpath, filename)
                mp3_name = os.path.splitext(filename)[0] + '.mp3'
                mp3_path = os.path.join(out_dir, mp3_name)
                if os.path.exists(mp3_path):
                    print(f"Skipping {mp3_path} (already exists)")
                    continue
                
                try:
                    # First check if video has audio using MoviePy
                    with VideoFileClip(video_path) as clip:
                        if clip.audio is None:
                            print(f"No audio in {video_path}, skipping.")
                            continue
                    
                    # Extract metadata from original video
                    print(f"Extracting metadata from {filename}...")
                    metadata = extract_metadata_from_video(video_path)
                    
                    # Convert using ffmpeg to preserve metadata
                    print(f"Converting {filename}...")
                    if convert_with_ffmpeg(video_path, mp3_path, metadata):
                        print(f"✅ Converted {video_path} -> {mp3_path}")
                        if metadata:
                            print(f"   📋 Preserved metadata: {', '.join(metadata.keys())}")
                    else:
                        # Fallback to MoviePy if ffmpeg fails
                        print("   ⚠️ FFmpeg failed, trying MoviePy fallback...")
                        with VideoFileClip(video_path) as clip:
                            clip.audio.write_audiofile(mp3_path)
                        print(f"   ✅ Converted with MoviePy: {video_path} -> {mp3_path}")
                        
                except Exception as e:
                    print(f"❌ Failed to convert {video_path}: {e}")

if __name__ == '__main__':
    check_dependencies()
    batch_convert_videos_to_mp3('.', 'completed')
