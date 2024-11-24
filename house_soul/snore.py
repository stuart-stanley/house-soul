from datetime import datetime
import pvporcupine
import pvrecorder
import pyttsx3
from secrets import get_pico_token
from assets import PorcupineWakeAssets
from logging import getLogger

log = getLogger(__name__)


class SleepingDog:
    """
    Let sleeping dogs lie... unless you want to wake up and do things!

    TODO: better hanlding of audio-index!
    """
    def __init__(self, audio_index=0):
        self.__pico_token = get_pico_token()
        self.__init_make_porcupine()
        self.__init_make_audio_in(audio_index)

    def __init_make_porcupine(self):
        wake_assets = PorcupineWakeAssets()

        keywords, voice_paths = wake_assets.get_keyword_and_file_lists()
        assert len(voice_paths) > 0, \
            'Did not find any porcupine wake assets.'

        rp = pvporcupine.create(
            access_key=self.__pico_token,
            keywords=keywords,
            keyword_paths=voice_paths
        )
        self.__porcupine = rp
        self.__keywords = keywords

    def __init_make_audio_in(self, audio_index):
        """
        make the pvrecorder audio in we will use. Note that
        we can't share one of these between different listeners thanks
        to the .frame_length...
        """
        audio_in = pvrecorder.PvRecorder(
            self.__porcupine.frame_length,
            device_index=audio_index
        )
        self.__audio_in = audio_in

    def wait_to_wake(self):
        """
        Time to turn around three times and lie down to sleep...
        """
        self.__audio_in.start()
        try:
            while True:
                audio_frame = self.__audio_in.read()
                keyword_index = self.__porcupine.process(audio_frame)

                if keyword_index >= 0:
                    log.info("Woke on %s(%d).", self.__keywords[keyword_index], keyword_index)
                    return self.__keywords[keyword_index]

        finally:
            self.__audio_in.stop()

    def cleanup(self):
        """
        cleanup resources
        """
        self.__audio_in.delete()
        self.__porcupine.delete()


def get_yapper():
    ttse = pyttsx3.init(debug=True)
    print("loopstart")
    ttse.say("starting")
    ttse.runAndWait()
    return ttse

if __name__ == '__main__':
    show_audio_devices()
    def wakeup_cb(yapper, keyword_index):
        print("yip yip yip!", keyword_index)
        yapper.say("yip yip yip!")
        yapper.runAndWait()
        print("back")

    yapper = get_yapper()
    zapper(yapper, wakeup_cb)
