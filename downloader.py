import yt_dlp
import os
import uuid

def download_youtube_video(url, download_dir='data/uploads'):
    """
    Downloads the video-only stream from YouTube.
    Returns the path to the downloaded file.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    file_id = str(uuid.uuid4())
    # We want video only as requested. mp4 format preferred for compatibility.
    # 'bestvideo[ext=mp4]/best[ext=mp4]/best' tries to get mp4 if possible.
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]/best[ext=mp4]/best',
        'outtmpl': os.path.join(download_dir, f'{file_id}.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename
