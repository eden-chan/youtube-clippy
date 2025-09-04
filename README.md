# YouTube Clippy (ytclip)

A fast and efficient YouTube video clip downloader that extracts specific time segments without downloading entire videos.

## Features

- **Stream-based clipping** - Downloads only the specified segment, not the entire video
- **Timestamp support** - Specify exact start and end times
- **Speed adjustment** - Change playback speed (0.5x to 4x)
- **QuickTime compatible** - Outputs H.264/AAC MP4 files
- **Minimal dependencies** - Just needs yt-dlp and ffmpeg

## Installation

### Prerequisites

You need to have `ffmpeg` installed on your system:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Install from PyPI

```bash
pip install youtube-clippy
```

### Install from source

```bash
git clone https://github.com/eden-chan/youtube-clippy.git
cd youtube-clippy
pip install -e .
```

## Usage

### Basic Usage

Download a clip from a YouTube video:

```bash
ytclip "https://youtu.be/VIDEO_ID" START_TIME END_TIME
```

### Examples

Extract clip from 1:30 to 2:45:
```bash
ytclip "https://youtu.be/dQw4w9WgXcQ" 1:30 2:45
```

Extract with custom output filename:
```bash
ytclip "https://youtu.be/dQw4w9WgXcQ" 1:30 2:45 -o my_clip.mp4
```

Extract at 1.5x speed:
```bash
ytclip "https://youtu.be/dQw4w9WgXcQ" 1:30 2:45 --speed 1.5
```

Extract from timestamp in HH:MM:SS format:
```bash
ytclip "https://youtu.be/dQw4w9WgXcQ" 1:23:45 1:24:30
```

### Command Line Options

```
positional arguments:
  url                   YouTube video URL
  start                 Start time (MM:SS or HH:MM:SS)
  end                   End time (MM:SS or HH:MM:SS)

optional arguments:
  -h, --help            Show help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filename (default: auto-generated)
  -s SPEED, --speed SPEED
                        Playback speed (e.g., 1.5 for 1.5x speed, 0.5 for half speed)
                        Range: 0.25 to 4.0 (default: 1.0)
  -v, --version         Show version number
```

## How It Works

Unlike traditional YouTube downloaders that fetch entire videos, `ytclip` uses ffmpeg's seeking capability to stream only the required segment. This means:

- **Faster downloads** - Only downloads what you need
- **Less bandwidth** - Saves data by not downloading unnecessary content
- **Less storage** - No temporary full-video files

The tool:
1. Extracts video metadata using yt-dlp
2. Calculates the exact byte range needed
3. Uses ffmpeg to stream and transcode only that segment
4. Outputs a properly formatted MP4 file

## Output Format

All clips are encoded as:
- **Video**: H.264 (libx264) with yuv420p pixel format
- **Audio**: AAC 
- **Container**: MP4 with faststart flag (optimized for streaming)

This ensures compatibility with all modern video players including:
- QuickTime Player
- VLC
- Windows Media Player
- Web browsers
- Mobile devices

## Speed Adjustment

The speed option maintains pitch correction for natural-sounding audio:
- **0.25x - 0.5x**: Slow motion with preserved audio pitch
- **0.5x - 2.0x**: Standard speed adjustment
- **2.0x - 4.0x**: Fast playback with intelligible audio

Note: Extreme speed changes may affect video quality.

## Troubleshooting

### "ffmpeg not found" error
Make sure ffmpeg is installed and in your system PATH:
```bash
ffmpeg -version
```

### "Video unavailable" error
- Check if the video is public and not geo-restricted
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### QuickTime compatibility issues
The tool automatically encodes to H.264/AAC which should work in QuickTime. If you still have issues, try:
```bash
ytclip "URL" START END -o clip.mp4
```

## Development

### Running from source
```bash
python -m ytclip.cli "URL" START END
```

### Running tests
```bash
python -m pytest tests/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube video extractor
- [FFmpeg](https://ffmpeg.org/) - Video processing

## Links

- **GitHub**: https://github.com/eden-chan/youtube-clippy
- **PyPI**: https://pypi.org/project/youtube-clippy/
- **Issues**: https://github.com/eden-chan/youtube-clippy/issues

## Changelog

### v1.0.0 (2024-01-09)
- Initial release
- Stream-based clip extraction
- Speed adjustment support
- QuickTime compatible output