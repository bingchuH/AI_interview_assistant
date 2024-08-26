import os
import threading
import azure.cognitiveservices.speech as speechsdk

# Azure Speech service credentials
SPEECH_KEY = os.getenv('SPEECH_KEY')
SPEECH_REGION = os.getenv('SPEECH_REGION')

class MySpeechRecognitionListener:
    def __init__(self, id):
        self.id = id
        self.recognized_text = []
        self.running = True

    def on_sentence_end(self, text):
        if not self.running:
            return
        if text:
            self.recognized_text.append(text)
        print(text)

    def get_full_text(self):
        return ''.join(self.recognized_text)

    def reset_text(self):
        self.recognized_text = []

    def stop(self):
        self.running = False

def process_realtime(id, listener):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "zh-CN"  # 设置识别语言为中文

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    try:
        while listener.running:
            # print("You speak.")
            speech_recognition_result = speech_recognizer.recognize_once_async().get()

            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                listener.on_sentence_end(speech_recognition_result.text)
            # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            #     print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
            # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            #     cancellation_details = speech_recognition_result.cancellation_details
            #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
            #         print("Error details: {}".format(cancellation_details.error_details))
            #         print("Did you set the speech resource key and region values?")
    except Exception as e:
        print(e)

def start_asr(listener):
    recognizer_thread = threading.Thread(target=process_realtime, args=(0, listener))
    recognizer_thread.daemon = True 
    recognizer_thread.start()
    return recognizer_thread

if __name__ == "__main__":
    listener = MySpeechRecognitionListener(0)
    recognizer_thread = start_asr(listener)
    
    try:
        while True:
            # Keep the main thread alive to allow continuous recognition
            pass
    except KeyboardInterrupt:
        print("Stopping the recognition...")
        listener.stop()
        recognizer_thread.join()