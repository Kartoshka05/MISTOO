import requests
from requests.exceptions import RequestException

def get_video_details(video_id):
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'statistics,snippet',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        items = data['items'][0]
        video_details = {
            'title': items['snippet']['title'],
            'publishedAt': items['snippet']['publishedAt'],
            'likeCount': items['statistics'].get('likeCount', 0),
            'dislikeCount': items['statistics'].get('dislikeCount', 0),
            'viewCount': items['statistics'].get('viewCount', 0),
            'commentCount': items['statistics'].get('commentCount', 0)
        }
        return video_details
    except (KeyError, IndexError):
        print(f"Unable to fetch video details for ID {video_id}.")
        return {}

def get_subscriber_count(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'statistics',
        'id': channel_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    try:
        subscriber_count = data['items'][0]['statistics']['subscriberCount']
        return subscriber_count
    except (KeyError, IndexError):
        print(f"Unable to fetch subscriber count for ID {channel_id}.")
        return None

def get_channel_name_by_id(channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'snippet',
        'id': channel_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    try:
        channel_name = data['items'][0]['snippet']['title']
        return channel_name
    except (KeyError, IndexError):
        print(f'Channel with ID {channel_id} not found.')
        return None

def get_latest_videos(channel_id, max_results=5):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': API_KEY,
        'channelId': channel_id,
        'part': 'snippet',
        'order': 'date',
        'maxResults': max_results,
        'type': 'video'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        videos = response.json().get('items', [])
        video_ids = [video['id']['videoId'] for video in videos]
        return video_ids
    except RequestException as e:
        print(f"Помилка при зверненні до YouTube API: {e}")
        return []
