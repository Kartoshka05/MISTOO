import os
import configparser
from file_manager import read_channels
from youtube_api import get_channel_name_by_id, get_latest_videos
from video_downloader import download_video
from csv_manager import ensure_csv_exists, update_csv
from translate_srt_to_ukr import translate_srt_with_openai


# Read configurations from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = os.environ.get('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables.")

import youtube_api
import file_manager

youtube_api.API_KEY = API_KEY
file_manager.API_KEY = API_KEY

SAVE_PATH = config['DEFAULT']['SAVE_PATH']
MAX_RESULTS = int(config['DEFAULT']['MAX_RESULTS'])
CSV_FILE = os.path.join(SAVE_PATH, "downloaded_videos.csv")

# Ensure the SAVE_PATH and CSV file exists
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
ensure_csv_exists(CSV_FILE)

if __name__ == "__main__":
    try:
        channels = read_channels("channels.txt")
        video_counter = 1  # For Номер
        for channel_id in channels:
            channel_name = get_channel_name_by_id(channel_id)
            if not channel_name:
                print(f"Unable to fetch channel name for ID {channel_id}. Skipping.")
                continue

            print(f"Using Channel ID: {channel_id}")
            latest_videos = get_latest_videos(channel_id, MAX_RESULTS)
            for video_id in latest_videos:
                download_video(video_id, channel_id, channel_name, SAVE_PATH, CSV_FILE)
                srt_path = os.path.join(video_folder, f"{video_filename}.srt")
                translate_srt_with_openai(srt_path)

                # Добавляем код для создания .txt файла
                txt_filename = os.path.join(video_folder, f"{video_filename}_ukr.txt")
                with open(txt_filename, 'w', encoding='utf-8') as txt_file:
                    with open(srt_path.replace(".srt", "_ukr.srt"), 'r', encoding='utf-8') as srt_file:
                        for line in srt_file:
                            if not re.match(r"^\d+$", line.strip()) and not re.match(r"^\d+\.\d+ --> \d+\.\d+$", line.strip()):
                                txt_file.write(line)

                video_counter += 1
    except Exception as e:
        print(f"Несподівана помилка: {e}")
