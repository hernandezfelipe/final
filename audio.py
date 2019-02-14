import sounddevice as sd
from datetime import datetime


def get_time():

    now = datetime.now()
    time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
    
    return time_id


def get_id():

    dev = sd.query_devices()
    
    dev_list = [dev[i]["name"] for i in range(5)]
    
    for i in range(len(dev_list)):
    
        if "USB" in dev_list[i]:
        
            return i
            
    print("Nenhum dispositivo foi encontrado")
    
    return -1

def bark(duration = 0.2):

    device = sd.query_devices()[get_id()]
    fs = int(device["default_samplerate"])
    rec = sd.rec(int((duration * fs)), samplerate = fs, channels=2)
    sd.wait()
    
    return rec.max()
    
if __name__ == "__main__":

    v = bark()
    print(v)
    
       

