import sounddevice as sd


def get_id():

    dev = sd.query_devices()
    
    dev_list = [dev[i]["name"] for i in range(5)]
    
    for i in range(len(dev_list)):
    
        if "USB" in dev_list[i]:
        
            return i
            
    print("Nenhum dispositivo foi encontrado")
    
    return -1

def bark():

    device = sd.query_devices()[get_id()]
    fs = int(device["default_samplerate"])
    duration = 1
    rec = sd.rec((int(duration) * fs), samplerate = fs, channels=1)
    sd.wait()
            
    return rec.max()
        
        
if __name__ == "__main__":

    pass
        
    
       

