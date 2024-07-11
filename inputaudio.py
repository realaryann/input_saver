'''
cmd-line args
arg1 = duration of recording
'''
import sys
import sounddevice as sd
import find_device as fd 
import numpy
import keyboard
from scipy.io.wavfile import write
import voskcall as v

def write_audio(recording, freq_aud) -> None:
	storage = f"./recordings/recording.wav"
	write(storage, freq_aud, recording)

def record_audio(freq_aud: int, duration: int):
	recording = sd.rec(int(duration*freq_aud), samplerate = freq_aud, channels=1)
	sd.wait()
	return recording

def read_keyboard():
	while True:
		if keyboard.is_pressed('r'):
			return 5
		elif keyboard.is_pressed('t'):
			return 10
		elif keyboard.is_pressed('y'):
			return 20
		elif keyboard.is_pressed('z'):
			exit()

def main():
	# Frequency of audio
	freq_aud = 44100
	duration = 0
	while True:
		print("R: 5 Seconds")
		print("T: 10 Seconds")
		print("Y: 20 Seconds")
		print("Z: Exit Program")
		print("\nINFO: Reading from the keyboard now")
		duration = read_keyboard()

		try:
			sd.default.device = fd.find_device()
		except Exception as e:
			print(f"Finding {fd.DEVICE_NAME} failed: {e}\n")

		try:
			print(f"INFO: Recording now, for {duration} seconds")
			recording = record_audio(freq_aud, duration)
		except Exception as e:
			print(f"Recording audio failed: {e}\n")

		try:
			write_audio(recording, freq_aud)
		except Exception as e:
			print(f"Writing audio failed: {e}\n")

		try:
			filename = "recordings/recording.wav"
			model_path = "/home/csrobot/vosktest/models/vosk-model-en-us-0.22"

			transcriber = v.Transcriber(model_path)
			transcription = transcriber.transcribe(filename)

			newf = "test.txt"

			filesrc = f"./results/{newf}"
			with open(filesrc, "w") as tf:
				for i in transcription:
					tf.write(i+'\n')
		except Exception as e:
			print("ERROR: Error while transcribing the recording")

if __name__ == "__main__":
	main()