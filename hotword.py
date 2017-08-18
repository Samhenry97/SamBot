import signal, time, subprocess
import snowboy.snowboydecoder as snowboydecoder, speech_recognition as sr
import glob, reply

detector = None
micIndex = 0

def hotwordDetected():
    if glob.pause:
        return
    else:
        glob.pause = True
    
    global detector
    detector.terminate()
    del detector
    
    text = voiceRecognition()
    userInfo = glob.db.getUserById(glob.ADMIN_IDS[0])
    chat = glob.db.getChat(131453030, userInfo['type'])
    response = reply.getReply(131453030, text, userInfo, chat)
    print('\tMessage: ', text)
    print('\tResponse: ', response)
    if response.strip():
        glob.say(response)
    else:
        glob.say('Sorry, I didn\'t get that.')
    
    glob.pause = False
    
    listen()
    
def voiceRecognition():
    tries = 0
    while tries < 3:
        try:
            r = sr.Recognizer()
            # r.dynamic_energy_threshold = False
            m = sr.Microphone(device_index=micIndex)
            with m as source: r.adjust_for_ambient_noise(source)
            subprocess.call(glob.ESPEAK_OPTIONS + ['Yes?'])
            with m as source: audio = r.listen(source, timeout=20, phrase_time_limit=10)
            print('Processing Voice...')
            return r.recognize_google(audio)
        except Exception as e:
            print('Oops, trying again:', e)
            tries += 1
        finally:
            try: del m
            except: pass
            try: del r
            except: pass
            try: del audio
            except: pass
    return ''

def init():
    global micIndex
    while True:
        try:
            micIndex = sr.Microphone.list_microphone_names().index('USB PnP Audio Device: Audio (hw:1,0)')
            break
        except:
            time.sleep(1)

def listen():
    global detector
    print('Listening for hotword...\n')
    detector = snowboydecoder.HotwordDetector('snowboy/resources/sambot.pmdl', sensitivity=0.6)
    detector.start(detected_callback=hotwordDetected, sleep_time=0.03)
