import json
import os
from pytube import YouTube
from pytube.exceptions import PytubeError
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta

def clean_filename(filename):
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_video(video_id, channel_id, channel_name, SAVE_PATH, CSV_FILE):

    from youtube_api import get_subscriber_count, get_video_details

    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        yt = YouTube(yt_url)
        ys = yt.streams.get_highest_resolution()
        
        video_number = len(os.listdir(SAVE_PATH)) + 1
        
        # Check if a folder with the video title already exists in the channel folder
        existing_folders = os.listdir(SAVE_PATH)
        for folder in existing_folders:
            if yt.title in folder:
                print(f"Відео {yt.title} вже існує. Пропускаю завантаження.")
                return
        
        clean_title = clean_filename(yt.title)
        video_filename = f"{video_number:04d}_{clean_title}"
        video_folder = os.path.join(SAVE_PATH, video_filename)
        os.makedirs(video_folder)  # Create a folder for each video

        save_file_path = os.path.join(video_folder, f"{video_filename}.mp4")

        if not os.path.exists(save_file_path):
            print(f"Скачивание {video_id} от {channel_name}...")
            ys.download(video_folder)
            print("Скачивание завершено!")

            # Save video description as JSON
            description_data = {
                "title": yt.title,
                "description": yt.description,
                "publish_date": yt.publish_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            description_filename = os.path.join(video_folder, f"{video_filename}.json")
            with open(description_filename, 'w', encoding='utf-8') as desc_file:
                json.dump(description_data, desc_file, ensure_ascii=False, indent=4)

            # Save subtitles as SRT
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                srt_data = "\n".join([f"{i+1}\n{subtitle['start']} --> {subtitle['start'] + subtitle['duration']}\n{subtitle['text']}" for i, subtitle in enumerate(transcript)])

                subtitles_filename = os.path.join(video_folder, f"{video_filename}.srt")
                with open(subtitles_filename, 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_data)
            except Exception as subtitle_error:
                print(f"Ошибка при скачивании субтитров: {subtitle_error}")
                
            subscriber_count = get_subscriber_count(channel_id)
            
            video_details = get_video_details(video_id)
            
            duration = str(timedelta(seconds=yt.length)) 
            # Fetch additional video data (likes, views, etc.)
            video_data = {
                "publishedAt": yt.publish_date.strftime('%Y-%m-%d %H:%M:%S'),
                "duration": duration,
                "viewCount": yt.views,
                "likeCount": video_details["likeCount"],
                "subscribers": subscriber_count,
                "commentCount": video_details["commentCount"]
            }

            # Update the CSV file
            from csv_manager import update_csv  # This import is inside to avoid circular dependency
            update_csv(CSV_FILE, video_id, channel_name, yt.title, video_data, video_number)
        else:
            print(f"Відео з ідентифікатором {video_id} вже існує у директорії {video_folder}. Пропускаю завантаження.")
    except PytubeError as e:
        print(f"Помилка при завантаженні відео {video_id}: {e}")
