# coding: utf-8
import pyaudio    # interact with micro
import tempfile   # interact with temp file
import wave       # save file audio
import audioop    # interact with raw data audio, get RMS

import apppath
import tts

# Microphone stream config.
CHUNK = 1024                    # CHUNKS buffer bytes read form mic each
FORMAT = pyaudio.paInt16        # audio format for WAV file
CHANNELS = 1                    # audio channels
RATE = 16000                    # Bit rate 16000kbps

class Mic():
    def __init__(self, stt):
        self.audio = pyaudio.PyAudio()
        self.stt = stt

    def passiveListen(self, keyword):
        """
        Passive listen keyword.

        Return:
        - THRESHOLD if listened keyword
        - None if don't
        """

        # new audio stream
        stream = self.audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

        # time to get RMS of enviroment
        THRESHOLD_TIME = 1          
        listRms = []
        # get data from stream
        for i in range (0, int(RATE / CHUNK * THRESHOLD_TIME)):
            data = stream.read(CHUNK)
            listRms.append(audioop.rms(data, 2))

        # get RMS average in 1s
        averageRms = sum(listRms) / len(listRms)
        # threshold speech
        THRESHOLD = averageRms * 1.8 
        # time out to listen keyword
        LISTEN_TIME = 10

        frames = []
        isDetected = False

        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            data = stream.read(CHUNK)
            frames.append(data)
            rms = audioop.rms(data, 2)
            if rms > THRESHOLD:
                isDetected = True
                break;

        # didn't detect speech
        if not isDetected:
            stream.stop_stream()
            stream.close()
            print "Cannot detected"
            return None

        # get data 1s before speech to detect
        frames = frames[-15:]
        DELAY_TIME = 1

        # record 1s after speech to detect
        for i in range(0, RATE / CHUNK * DELAY_TIME):
            data = stream.read(CHUNK)
            frames.append(data)

        # save temp file
        with tempfile.SpooledTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(CHANNELS)
            wav_fp.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(''.join(frames))
            wav_fp.close()
            f.seek(0)

            transcripts = self.stt.get_value(f)
        stream.stop_stream()
        stream.close()
        print transcripts
        if transcripts:
            if any(keyword == pharse for pharse in transcripts):
                return THRESHOLD
        
        return None

    def activeListen(self):
        """listen command of user when JarvisPi is called."""

        stream = self.audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

        LISTEN_TIME = 3
        frames = []

        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        tts.speak(apppath.get_resources('beep.wav'))

        with tempfile.SpooledTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(CHANNELS)
            wav_fp.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(''.join(frames))
            wav_fp.close()
            f.seek(0)
            
            transcripts = self.stt.get_value(f)
            print transcripts
            return transcripts
        
