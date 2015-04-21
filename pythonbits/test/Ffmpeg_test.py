import os
import glob
from tempfile import mkdtemp, NamedTemporaryFile
import re
import subprocess

import mock
from nose.tools import raises

from pythonbits.Ffmpeg import FFMpeg, FFMpegException


FIXTURE_VIDEO = 'pythonbits/test/video.mp4'
_real_popen = subprocess.Popen


def popen_no_environ(*args, **kwargs):
    kwargs['env'] = {}
    return _real_popen(*args, **kwargs)


@mock.patch('subprocess.Popen', new=popen_no_environ)
def test_raises_when_no_ffmpeg_in_path():
    f = NamedTemporaryFile()
    try:
        FFMpeg(f.name).duration()
    except FFMpegException as e:
        assert 'Ffmpeg not installed' in str(e)
    finally:
        f.close()


def test_raises_when_file_is_invalid():
    f = NamedTemporaryFile()
    try:
        FFMpeg(f.name).duration()
    except FFMpegException as e:
        assert 'Duration' in str(e)
    finally:
        f.close()

    dumpfiles = glob.glob('ffmpeg-error-dump-*')
    assert dumpfiles
    for file in dumpfiles:
        os.unlink(file)


def test_parses_correct_duration_as_int():
    assert FFMpeg(FIXTURE_VIDEO).duration == 5


def test_screenshot_files_are_created():
    shots = 2
    image_files = FFMpeg(FIXTURE_VIDEO).takeScreenshots(shots)
    assert len(image_files) == shots
    assert all(os.path.exists(image) for image in image_files)
