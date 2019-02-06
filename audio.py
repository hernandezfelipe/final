import sounddevice as sd

def bark():

    device = sd.query_devices()[3]
    fs = int(device["default_samplerate"])
    duration = 1
    rec = sd.rec((int(duration) * fs), samplerate = fs, channels=1)
    sd.wait()
            
    return rec.max()
        
   
    

