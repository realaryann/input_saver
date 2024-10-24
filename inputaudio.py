'''
cmd-line args
arg1 = duration of recording
'''
import sys
import numpy
import sounddevice as sd
from scipy.io.wavfile import write
import voskcall as v
import find_device as fd 

def write_audio(recording, freq_aud) -> None:
    storage = "./recordings/recording.wav"
    write(storage, freq_aud, recording)

def record_audio(freq_aud: int, duration: int):
    recording = sd.rec(int(duration*freq_aud), samplerate = freq_aud, channels=1)
    sd.wait()
    return recording

def validate(duration):
    if duration in "rR":
        return 5
    elif duration in "tT":
        return 10
    elif duration in "yY":
        return 20
    elif duration in "zZ":
        return -1
    return -1

def record_manager(freq_aud, duration):
    try:
        print(f"INFO: Recording now, for {duration} seconds")
        recording = record_audio(freq_aud, duration)
        return recording
    except Exception as e:
        raise RuntimeError(f"Recording audio failed: {e}\n")

def write_manager(freq_aud, recording):
    try:
        print("INFO: Writing audio to file now")
        write_audio(recording, freq_aud)
    except Exception as e:
        raise RuntimeError(f"Writing audio failed: {e}\n")

def main():
    # Frequency of audio
    freq_aud = 44100
    duration = 0
    while True:
        print("R: 5 Seconds")
        print("T: 10 Seconds") 
        print("Y: 20 Seconds")
        print("Z: Exit Program")
        duration = input("Enter Key: ")
        while duration not in "rRtTyYzZ":
            duration = input("Enter Key: ")
        duration = validate(duration)
        if duration == -1:
            sys.exit()
        print("INFO: Finding device")
        try:
            sd.default.device = fd.find_device()
            print("INFO: Found audio device")
        except Exception as e:
            raise RuntimeError(f"Finding {fd.DEVICE_NAME} failed: {e}\n")
        recording = record_manager(freq_aud, duration)
        write_manager(freq_aud, recording)

if __name__ == "__main__":
    main()
