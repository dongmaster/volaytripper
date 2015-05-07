#!/usr/bin/python3
from __future__ import unicode_literals
import youtube_dl
from volapi import Room
import sys
import os
import time

#myoc = Room("BEEPi", "test")
name = "JonTheRipper"
password = "pleaserapemyfaggotface"

def onmessage(msg):
    splitmsg = msg.msg.split(" ")

    if splitmsg[0] == ":rip" and len(splitmsg) == 2:
        upload_video(splitmsg[1], msg.nick)

def upload_video(video_url, nick):
    global room
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)


    def my_hook(d):
        if d['status'] == 'finished':
            video = room.upload_file(d["filename"])
            time.sleep(0.5)
            room.post_chat("{}, @{}".format(nick, video))
            os.remove("./{}".format(d["filename"]))

    ydl_opts = {
        'format': "mp4",
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Usage ./main.py <Room name>")
        sys.exit(1)

    room_name = sys.argv[1]

    while True:
        try:
            print("Started ripper")
            room = Room(room_name, name)
            room.user.login(password)
            room.add_listener("chat", onmessage)
            room.listen()
        # pylint: disable=broad-except
        except Exception:
            print("")



