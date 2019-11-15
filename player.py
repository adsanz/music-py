import socket 
import pyaudio
import wave
import struct
import time

#### FLAGS #####
chunk = 2048
stop = 0
start = 0
skip = 0
scan = 0

def ConnectSocket(address,port):
    s = socket.socket()
    s.connect((address,port))
    return s

def GetWaveDetails():
    sc2 = ConnectSocket("localhost",2225)
    data2 = b''
    while True:
        part = sc2.recv(chunk)
        data2 += part
        if not part:
            break
    return struct.unpack("III", data2)

format_wav,framerate_wav,channels_wav = GetWaveDetails()
#print(format_wav,channels_wav,framerate_wav)


p = pyaudio.PyAudio()
stream = p.open(
    format = format_wav,
    channels = channels_wav,
    rate = framerate_wav,
    output = True)


sc = ConnectSocket("localhost",9995)
while True:
    part = sc.recv(chunk)
    stream.write(part)
    if not part:
        break
sc.close()
stream.close()
p.terminate()
