import socket 
import pyaudio
import wave
from pydub import AudioSegment
import struct


#### FLAGS #####
chunk = 2048
stop = 0
start = 0
skip = 0
scan = 0
song = "ctangana-sundays.wav"

#### FUNCTIONS ####
def ConvertWav(song):
    sound = AudioSegment.from_mp3(song)
    sound.export(song.replace("mp3","wav"), format="wav")

def CreateSocket(address,port):
    s = socket.socket()
    s.bind((address,port))
    s.listen(12)
    return s.accept()

def SendWaveDetails(song,host,port):
    try:
        file = wave.open(song)
    except wave.Error:
        print("selected song is on mp3, converting to wav")
        ConvertWav(song)
        print("converted sucessfully")
        file = wave.open(song.replace("mp3", "wav"))
    sc2,address2 = CreateSocket(host,port) 
    data = struct.pack("III", p.get_format_from_width(file.getsampwidth()),file.getframerate(),file.getnchannels())
    sc2.send(data)
    file.close()

p = pyaudio.PyAudio()
SendWaveDetails(song,host="localhost",port=2225)
sc,address = CreateSocket("localhost",9995)
file = wave.open("ctangana-sundays.wav", "rb")
data2 = b''
print(data2)
while True:
    sc.send(data2)
    data2 = file.readframes(chunk)
    if not data2:
        break
sc.close()
file.close()
p.terminate()