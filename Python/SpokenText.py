import speech_recognition as sr
#import pyaudio

r = sr.Recognizer()

#p = pyaudio.PyAudio()

# for i in range(p.get_device_count()):
# print(p.get_device_info_by_index(i))


def SpokenText():

    with sr.Microphone() as source:
        print("Ouvindo... ")
        print(type(source))
        r.adjust_for_ambient_noise(source, 0.5)  # Adjust for ambient
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="pt-BR")
        # print(text)
        return text
    except Exception:
        return False


while True:
    print(SpokenText())
