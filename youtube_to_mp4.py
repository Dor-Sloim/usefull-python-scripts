"""
    Downloads a youtube video converted to .mp4
    And opens in media player player.

    Setup:
        pip install pytube3
        pip install pyautogui


    Usage:
        python youtube_to_mp4.py

    Example input:
        https://youtu.be/ymjNGjuBCTo

"""
import os
import time
import webbrowser

import pyautogui
from pytube import YouTube
from pytube.exceptions import RegexMatchError


def get_video_path():
    r"""

    :return: Creates C:\Users\user\Videos\Youtube
             And returns the path to it.

    """
    try:
        home = os.path.expanduser('~')
        video_folder = os.path.join(home, 'Videos')
        youtube_dir_path = os.path.join(video_folder, 'Youtube')
        os.makedirs(youtube_dir_path, exist_ok=True)

        return youtube_dir_path
    except:
        return video_folder


DEST_FOLDER = get_video_path()


def open_video_folder(vid_path):
    """
        Open the folder in Explorer,
        and then plays the video.
    :param filename: The path to the downloaded video.
    :return: None
    """
    webbrowser.open('file:///' + DEST_FOLDER)
    time.sleep(1)
    webbrowser.open(vid_path)
    time.sleep(2)


def maximize_vlc_video(window):
    try:
        window.activate()
        window.maximize()
    except:
        pass


def get_vlc_window():
    try:
        return [window for window in pyautogui.getAllWindows() if 'VLC' in window.title][0]
    except:
        pass


def main():
    try:
        vid_url = input('Enter YouTube video URL: ').strip()
        youtube = YouTube(vid_url)
    except RegexMatchError:
        print('Invalid YouTube URL!')
        return

    print(f'Downloading {youtube.title} ...')
    video_stream = youtube.streams.first()
    video_len_str = time.strftime('%M:%S', time.gmtime(video_stream._monostate.duration))
    print(f'Video Length: {video_len_str}')
    downloaded_path = video_stream.download(DEST_FOLDER)

    open_video_folder(downloaded_path)
    print('Downloaded successfully !')

    maximize_vlc_video(get_vlc_window())


if __name__ == '__main__':
    main()
