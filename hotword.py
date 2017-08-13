import snowboy.snowboydecoder as snowboydecoder
import speech_recognition as sr
import signal, time, subprocess
import glob, reply

detector = None
index = device_index=sr.Microphone.list_microphone_names().index('USB PnP Audio Device: Audio (hw:1,0)')

def hotwordDetected():
    global detector
    detector.terminate()
    del detector
    
    while True:
        try:
            r = sr.Recognizer()
            m = sr.Microphone(device_index=index)
            with m as source: r.adjust_for_ambient_noise(source)
            subprocess.call(['espeak', 'Yes, Sam?'])
            with m as source: audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print('Processing Voice...')
            del m
            if audio is None:
                print('None')
                raise
            text = r.recognize_google(audio)
            break
        except Exception as e:
            print('Oops, trying again:', e)
        finally:
            try: del m
            except: pass
            try: del r
            except: pass
    
    userInfo = { 'id': glob.ADMIN_ID, 'first_name': 'Samuel', 'last_name': 'Henry', 'username': 'SamHenry97', 'language_code': 'en-US' }
    response = reply.getReply(glob.ADMIN_ID, text, userInfo)
    print('\tMessage: ', text)
    print('\tResponse: ', response)
    if response.strip():
        glob.say(response)
    else:
        glob.say('Sorry, I didn\'t get that.')
    
    init()

def init():
    global detector
    print('Hotword Detection Initialized...')
    detector = snowboydecoder.HotwordDetector('snowboy/resources/sambot.pmdl', sensitivity=0.5)
    detector.start(detected_callback=hotwordDetected, sleep_time=0.03)
