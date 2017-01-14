#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
    >>> python test.py test.mp3
'''
from acrcloud.recognizer import ACRCloudRecognizer

def audio_file(audio):

    config = {
        'host': 'ap-southeast-1.api.acrcloud.com',
        'access_key': 'f1840ce5b0603e9db3ec8c526eea65e5',
        'access_secret': '1NfVJoxoREbGlO9HVqG4QNkSiMT86Lvs3Geogov9',
        'debug': True,
        'timeout': 30  # seconds
    }

    '''This module can recognize ACRCloud by most of audio/video file.
        Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
        Video: mp4, mkv, wmv, flv, ts, avi ...'''
    re = ACRCloudRecognizer(config)

    # recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].

    buf = open(audio, 'rb').read()
    # recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
    return re.recognize_by_filebuffer(buf,1)
    # aa.wav must be (RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    # buf = open('aa.wav', 'rb').read()
    # buft = buf[1024000:192000+1024001]
    # recognize by audio_buffer(RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz)
    # print re.recognize(buft)
