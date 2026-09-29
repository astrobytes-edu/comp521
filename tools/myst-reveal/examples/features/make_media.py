"""Regenerate the small, locally authored media fixtures; requires ffmpeg."""
import math
import os
from pathlib import Path
import struct
import subprocess
import wave

ROOT = Path(__file__).resolve().parent
with wave.open(str(ROOT / 'tone.wav'), 'wb') as wav:
    wav.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
    wav.writeframes(b''.join(struct.pack('<h', int(1800 * math.sin(2 * math.pi * 440 * i / 16000))) for i in range(16000)))

width, height, frames = 480, 160, 60
raw = bytearray()
for frame in range(frames):
    center = 20 + frame * (width - 40) / (frames - 1)
    for y in range(height):
        for x in range(width):
            raw.extend((47, 111, 111) if (x - center) ** 2 + (y - 80) ** 2 < 15 ** 2 else (238, 241, 245))
subprocess.run([os.environ.get('FFMPEG', 'ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'rawvideo', '-pixel_format', 'rgb24', '-video_size', f'{width}x{height}',
    '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', str(ROOT / 'motion.mp4')], input=bytes(raw), check=True)
