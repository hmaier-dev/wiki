---
categories:
- cli
- Linux
title: ffmpeg
---

# ffmpeg

## Converting filetypes
If you want to convert a single ogg-file into mp3.
```bash
ffmpeg -i "file.ogg" "file.mp3"
```
If there are multiple files, instead of writing a script, you could use gnu/parallel to use all of your CPU cores.
```bash
parallel ffmpeg -i "{}" "{.}.mp3" ::: *.ogg
```
## Changing bitrate

```bash
ffmpeg -i sounds.mp3 -b:a 128k sounds.mp3
```
These are the different bitrates.

- 32 kbps: Very low quality, generally used for voice recordings or very small files.
- 64 kbps: Low quality, suitable for voice recordings and some music where size is a significant concern.
- 96 kbps: Moderate quality, often used for streaming audio over low-bandwidth connections.
- 128 kbps: Standard quality, often considered the minimum acceptable quality for music. A common choice for streaming and digital downloads.
- 160 kbps: Above average quality, providing better sound than 128 kbps but with a slightly larger file size.
- 192 kbps: Good quality, often used for higher-quality music streaming and digital downloads.
- 224 kbps: Higher quality, offering better audio fidelity than 192 kbps.
- 256 kbps: High quality, used for better sound reproduction, often used in high-quality digital downloads.
- 320 kbps: Highest quality for MP3, offering the best audio fidelity, often indistinguishable from the original CD-quality sound.

