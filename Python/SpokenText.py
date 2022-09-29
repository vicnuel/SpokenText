import speech_recognition as sr
#import pyaudio

r = sr.Recognizer()

#p = pyaudio.PyAudio()

#for i in range(p.get_device_count()):
    #print(p.get_device_info_by_index(i))


def SpokenText():
    
    with sr.Microphone(1) as source:
        print("Ouvindo... ")
        r.adjust_for_ambient_noise(source, 1)  # Adjust for ambient
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="pt-BR")
        print(text)
        return text
    except Exception:
        return False


#while True:
    #print(Spoken_Text())