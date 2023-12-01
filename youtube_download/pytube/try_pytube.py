import argparse
import ssl
import traceback
ssl._create_default_https_context = ssl._create_unverified_context
from pytube import YouTube

VIDEO_SAVE_DIRECTORY = "./videos"
AUDIO_SAVE_DIRECTORY = "./audio"

MAX_RETRIES = 3  # 最大重试次数

class BooleanOptionalAction(argparse.Action):
    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        super(BooleanOptionalAction, self).__init__(
            option_strings, dest, nargs=0, const=True, default=default, required=required, help=help
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


def download(video_url, resolution=None):
    video = YouTube(video_url)

    if resolution:
        video = video.streams.filter(res=resolution).first()
    else:
        video = video.streams.get_highest_resolution()

    retries = 0

    while retries < MAX_RETRIES:
        try:
            video.download(VIDEO_SAVE_DIRECTORY)
            print(f"Video was downloaded successfully: {video_url}")
            break
        except:
            retries += 1
            print(f"Failed to download video: {video_url}")
            traceback.print_exc()


def download_audio(video_url):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio=True).first()

    retries = 0

    while retries < MAX_RETRIES:
        try:
            audio.download(AUDIO_SAVE_DIRECTORY)
            print(f"Audio was downloaded successfully: {video_url}")
            break
        except:
            retries += 1
            print(f"Failed to download audio: {video_url}")
            traceback.print_exc()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, nargs="+", help="URLs to YouTube videos")
    ap.add_argument("-a", "--audio", required=False, help="Download audio only", action=BooleanOptionalAction)
    ap.add_argument("-r", "--resolution", required=False, help="Video resolution (e.g., 1080p)")
    args = vars(ap.parse_args())

    video_urls = args["video"]

    if args["audio"]:
        for url in video_urls:
            download_audio(url)
    else:
        for url in video_urls:
            download(url, args["resolution"])

#  python try_pytube.py  -v "[https://youtu.be/v8ZsXIf2l3Y]"  -r 360p