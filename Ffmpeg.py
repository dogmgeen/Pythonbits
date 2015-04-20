#!/usr/bin/env python
# encoding: utf-8
"""
Ffmpeg.py

Created by Ichabond on 2012-07-01.
Copyright (c) 2012 Baconseed. All rights reserved.
"""
import os
import re
import subprocess
from tempfile import mkdtemp, NamedTemporaryFile


class FFMpegException(Exception):
    pass


class FFMpeg(object):

    def __init__(self, filepath):
        self.file = filepath
        self.tempdir = mkdtemp(prefix="pythonbits-")

    @property
    def duration(self):
        ffmpeg_data, __ = ffmpeg_wrapper([r"ffmpeg", "-i", self.file],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)

        ffmpeg_duration = re.findall(
            r'Duration:\D(\d{2}):(\d{2}):(\d{2})',
            ffmpeg_data)
        if ffmpeg_duration:
            hours, minutes, seconds = map(int, ffmpeg_duration[0])
            return hours * 3600 + minutes * 60 + seconds
        else:
            self._create_dump_and_panic(ffmpeg_data)

    def _create_dump_and_panic(self, ffmpeg_data):
        output_file = NamedTemporaryFile(prefix='ffmpeg-error-dump-',
                                         delete=False, dir='', mode='wb')
        with output_file as f:
            f.write(ffmpeg_data)

        err_msg = ("Expected ffmpeg to mention 'Duration' but it did not. "
                   "Please copy the contents of '%s' to http://pastebin.com/ "
                   "and send the pastebin link to the bB forum."
                   % output_file.name)
        raise FFMpegException(err_msg)

    def takeScreenshots(self, shots):
        stops = range(20, 81, 60 / (shots - 1))
        imgs = [os.path.join(self.tempdir, "screen%s.png" % stop)
                for stop in stops]

        duration = self.duration
        for img, stop in zip(imgs, stops):
            ffmpeg_wrapper([r"ffmpeg",
                            "-ss", str((duration * stop) / 100),
                            "-i", self.file,
                            "-vframes", "1",
                            "-y",
                            "-f",
                            "image2", img],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return imgs


def ffmpeg_wrapper(*args, **kwargs):
    try:
        return subprocess.Popen(*args, **kwargs).communicate()
    except OSError:
        raise FFMpegException("Error: Ffmpeg not installed, refer to "
                              "http://www.ffmpeg.org/download.html for "
                              "installation")
