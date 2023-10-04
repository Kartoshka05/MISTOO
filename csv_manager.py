import csv
import datetime
import os

FIELDNAMES = [
    "Номер",
    "Название",
    "Канал",
    "Дата скачивания",
    "Дата загрузки на YouTube",
    "Длительность видео",
    "Количество просмотров",
    "Лайки",
    "Подписчики",
    "Комментарии"
]

def ensure_csv_exists(CSV_FILE):
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()

def update_csv(CSV_FILE, video_id, channel_name, video_title, video_data, number):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        
        row_data = {
            "Номер": str(number).zfill(4),
            "Название": video_title,
            "Канал": channel_name,
            "Дата скачивания": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Дата загрузки на YouTube": video_data.get('publishedAt', ""),
            "Длительность видео": video_data.get('duration', ""),
            "Количество просмотров": video_data.get('viewCount', ""),
            "Лайки": video_data.get('likeCount', ""),
            "Подписчики": video_data.get('subscribers', ""),
            "Комментарии": video_data.get('commentCount', "")
        }
        writer.writerow(row_data)

