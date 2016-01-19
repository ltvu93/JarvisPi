# coding: utf-8
import pyaudio    # interact with micro
import tempfile   # interact with temp file
import wave       # save file audio
import audioop    # interact with raw data audio, get RMS

import apppath
from tts import OnlineTTS

# Microphone stream config.
CHUNK = 1024                    # CHUNKS buffer bytes read form mic each
FORMAT = pyaudio.paInt16        # audio format for WAV file
CHANNELS = 1                    # audio channels
RATE = 16000                    # Bit rate 16000kbps

class Mic():
    def __init__(self, passive_stt, active_stt):
        self.audio = pyaudio.PyAudio()
		self.passive_stt = passive_stt
		self.active_stt = active_stt

    def passiveListen_old(self, keyword):
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
								
		self.passive_stt.listen_hot_keyword(keyword, stream)
	
	def fetchThreshold(self):

        # TODO: Consolidate variables from the next three functions
        THRESHOLD_MULTIPLIER = 1.8
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(20)]

        # calculate the long run average, and thereby the proper threshold
        for i in range(0, RATE / CHUNK * THRESHOLD_TIME):

            data = stream.read(CHUNK)
            frames.append(data)

            # save this data point as a score
            lastN.pop(0)
            lastN.append(self.getScore(data))
            average = sum(lastN) / len(lastN)

        stream.stop_stream()
        stream.close()

        # this will be the benchmark to cause a disturbance over!
        THRESHOLD = average * THRESHOLD_MULTIPLIER

        return THRESHOLD
	
	def activeListen(self):
		options = activeListenAllOptions()
		if options:
			return options[0]
			
    def activeListenToAllOptions(self):
        """listen command of user when JarvisPi is called."""

		THRESHOLD = self.fetchThreshold()
		
		tts.speak(apppath.get_resources('yes.mp3'))

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        frames = []
        # increasing the range # results in longer pause after command
        # generation
        lastN = [THRESHOLD * 1.2 for i in range(30)]

        for i in range(0, RATE / CHUNK * LISTEN_TIME):

            data = stream.read(CHUNK)
            frames.append(data)
            score = self.getScore(data)

            lastN.pop(0)
            lastN.append(score)

            average = sum(lastN) / float(len(lastN))

            # TODO: 0.8 should not be a MAGIC NUMBER!
            if average < THRESHOLD * 0.8:
                break

        # save the audio data
        stream.stop_stream()
        stream.close()
        self.tts.speak_long_sentence(apppath.get_resources('beep.wav'))

        with tempfile.SpooledTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(CHANNELS)
            wav_fp.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(''.join(frames))
            wav_fp.close()
            f.seek(0)
			
            tts.speak(apppath.get_resources('beep.wav'))
            return stt.gg_transale(f)