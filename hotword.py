import snowboy.snowboydecoder as snowboydecoder
import speech_recognition as sr
import signal, time, subprocess
import glob, reply

detector = snowboydecoder.HotwordDetector('snowboy/resources/sambot.pmdl', sensitivity=0.5)
r = sr.Recognizer()
index = device_index=sr.Microphone.list_microphone_names().index('USB PnP Audio Device: Audio (hw:1,0)')
print(index)
m = sr.Microphone(device_index=index)

def hotwordDetected():
    detector.terminate()
    
    while True:
        try:
            with m as source: r.adjust_for_ambient_noise(source)
            with m as source: audio = r.listen(source)
            break
        except:
            time.sleep(0.1)
    
    text = r.recognize_google(audio)
    userInfo = { 'id': glob.ADMIN_ID, 'first_name': 'Samuel', 'last_name': 'Henry', 'username': 'SamHenry97', 'language_code': 'en-US' }
    response = reply.getReply(glob.ADMIN_ID, text, userInfo)
    glob.say(response)
    
    init()

def init():
    detector.start(detected_callback=hotwordDetected, sleep_time=0.03)
