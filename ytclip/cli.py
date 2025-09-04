#!/usr/bin/env python3
import yt_dlp
import argparse
import re
import sys
from urllib.parse import urlparse, parse_qs

def parse_time(time_str):
    """Convert time string (MM:SS or HH:MM:SS) to seconds"""
    parts = time_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    else:
        return int(parts[0])

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    parsed = urlparse(url)
    
    if 'youtube.com' in parsed.netloc:
        query = parse_qs(parsed.query)
        return query.get('v', [None])[0]
    elif 'youtu.be' in parsed.netloc:
        return parsed.path.lstrip('/')
    return None

def download_clip(url, start_time, end_time, output_name=None, speed=1.0):
    """Download a clip from YouTube video using ffmpeg for efficient streaming"""
    
    # Parse times
    start_seconds = parse_time(start_time)
    end_seconds = parse_time(end_time)
    duration = end_seconds - start_seconds
    
    # Set output filename
    if not output_name:
        # Get video info for title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            safe_title = re.sub(r'[^\w\s-]', '', info['title'])[:50]
            output_name = f"{safe_title}_clip_{start_time.replace(':', '-')}-{end_time.replace(':', '-')}.mp4"
    
    # Build ffmpeg command with speed adjustment
    ffmpeg_input_args = [
        '-ss', str(start_seconds),  # Seek to start time (before input for fast seeking)
    ]
    
    ffmpeg_output_args = [
        '-t', str(duration),        # Duration to capture
        '-c:v', 'libx264',          # H.264 video codec for QuickTime compatibility
        '-c:a', 'aac',              # AAC audio codec for QuickTime compatibility
        '-preset', 'fast',          # Encoding preset
        '-crf', '23',               # Quality (lower = better, 23 is default)
        '-pix_fmt', 'yuv420p',      # Pixel format for compatibility
        '-movflags', '+faststart',  # Optimize for streaming
    ]
    
    # Add speed adjustment filters if needed
    if speed != 1.0:
        video_filter = f"setpts={1/speed}*PTS"
        audio_filter = f"atempo={speed}"
        
        # For speeds > 2.0, we need to chain atempo filters
        if speed > 2.0:
            chain_count = int(speed / 2)
            remainder = speed / (2 ** chain_count)
            audio_filter = "atempo=2.0," * chain_count + f"atempo={remainder}"
        elif speed < 0.5:
            chain_count = int(1 / (speed * 2))
            remainder = 1 / (speed * (2 ** chain_count))
            audio_filter = "atempo=0.5," * chain_count + f"atempo={remainder}"
        
        ffmpeg_output_args.extend([
            '-filter:v', video_filter,
            '-filter:a', audio_filter,
        ])
    
    # Configure yt-dlp with external downloader (ffmpeg)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': False,
        'outtmpl': output_name,
        'external_downloader': 'ffmpeg',
        'external_downloader_args': {
            'ffmpeg_i1': ffmpeg_input_args,
            'ffmpeg_o': ffmpeg_output_args,
        },
    }
    
    # Download the clip
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📹 Streaming clip from {start_time} to {end_time}")
            if speed != 1.0:
                print(f"⚡ Applying {speed}x speed")
            ydl.download([url])
        print(f"\n✓ Clip saved as: {output_name}")
        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Download clips from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://youtu.be/0g3yo1DjiLM" 31:21 32:48
  %(prog)s "https://youtube.com/watch?v=abc123" 1:30 2:45 --speed 1.5
  %(prog)s "https://youtu.be/xyz789" 10:00 15:30 -o "my_clip.mp4" -s 2.0
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('start', help='Start time (MM:SS or HH:MM:SS)')
    parser.add_argument('end', help='End time (MM:SS or HH:MM:SS)')
    parser.add_argument('-o', '--output', help='Output filename (default: auto-generated)')
    parser.add_argument('-s', '--speed', type=float, default=1.0, 
                       help='Playback speed (e.g., 1.5 for 1.5x speed, 0.5 for half speed)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Validate URL
    video_id = extract_video_id(args.url)
    if not video_id:
        print("✗ Invalid YouTube URL")
        return 1
    
    # Reconstruct clean URL
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"📹 Video ID: {video_id}")
    print(f"⏱️  Clipping from {args.start} to {args.end}")
    if args.speed != 1.0:
        print(f"⚡ Speed: {args.speed}x")
    
    # Download the clip
    success = download_clip(clean_url, args.start, args.end, args.output, args.speed)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())