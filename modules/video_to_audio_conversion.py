import os
import subprocess
from utils.logger_config import setup_logger


logger = setup_logger(name=__name__, log_file="logs/app.log")


def extract_audio(input_video_path, extracted_audio_path=None):
    if extracted_audio_path is None:
        base_name = os.path.splitext(os.path.basename(input_video_path))[0]
        output_dir = os.path.dirname(input_video_path)
        extracted_audio_path = os.path.join(output_dir, f"{base_name}.mp3")

    command = [
        "ffmpeg", "-y",
        "-i", input_video_path,
        "-vn",
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",
        "-ac", "1",
        "-ar", "24000",
        extracted_audio_path
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")
    except Exception as e:
        raise RuntimeError(f"Error executing ffmpeg command: {e}")

    if not os.path.exists(extracted_audio_path):
        raise FileNotFoundError(f"Audio file was not created at {extracted_audio_path}")

    file_size_mb = os.path.getsize(extracted_audio_path) / (1024 * 1024)
    logger.info(f"Audio successfully extracted: {extracted_audio_path} (Size: {file_size_mb:.2f} MB)")

    if file_size_mb > 25:
        logger.warning(f"WARNING: Audio file is larger than 25MB ({file_size_mb:.2f} MB). "
              f"It will be split into chunks at the transcription step.")

    return extracted_audio_path
