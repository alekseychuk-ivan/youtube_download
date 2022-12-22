from pytube import YouTube
import os
from pathlib import Path
from datetime import datetime
from threading import Timer


patha = Path('output/audio')
pathv = Path('output/video')
pathr = Path('output/resume')


def download():
    with open('link.txt', 'r', encoding='utf-8') as file:
        file = file.readlines()

    for link in file:
        yt = YouTube(link)
        yt.streams.filter(res='1080p').first().download(pathv)
        yt.streams.filter(abr='128kbps').first().download(patha)

        for path in [patha, pathv]:
            for name in os.listdir(path):
                new_name = name.replace(' ', '_')
                os.replace('{}/{}'.format(path, name), '{}/{}'.format(path, new_name),)

        for name in os.listdir(patha):
            cmd = "ffmpeg -i {}/{} -i {}/{} -c:v copy {}/{}".format(pathv, name, patha, name, pathr, name)
            os.system(cmd)
            print('{} загружен в {}'.format(name, datetime.today()))
            for path in [pathv, patha]:
                file = Path("{}/{}".format(path, name))
                file.unlink()


def delay(secs):
    t = Timer(secs, download)
    t.start()


# x = datetime.today()
# if 2 <= x.hour <= 8:
#     download()
# elif x.hour < 2:
#     y = x.replace(day=x.day, hour=2, minute=0, second=0)
#     delta_t = y - x
#     secs = delta_t.seconds + 1
#     delay(secs)
# else:
#     y = x.replace(day=x.day + 1, hour=2, minute=0, second=0, microsecond=0)
#     delta_t = y - x
#     secs = delta_t.seconds + 1
#     delay(secs)

download()
