import pvrecorder
import pvrhino
import time
from secrets import get_pico_token
from assets import RhinoContextAssets
from logging import getLogger

log = getLogger(__name__)



class Interactor:
    """
    Note: crude 1st try, with a hope to move to plugin based...
    """
    _SLEEP_AFTER__S = 70.5
    
    def __init__(self, audio_index):
        self.__pico_token = get_pico_token()
        self.__init_make_rhino()
        self.__init_make_audio_in(audio_index)

    def __init_make_rhino(self):
        rhino_assets = RhinoContextAssets()

        context_paths = rhino_assets.get_file_list()
        assert len(context_paths) > 0, \
            'no rhino context files found.'
        if len(context_paths) > 1:
            # TODO: it might be possible to make N Rhinos?
            log.warn('found more than one rhino context (%s). Using 1st for now',
                     context_paths)
        self.__rhino = pvrhino.create(
            access_key=self.__pico_token,
            context_path=context_paths[0]
        )

    def __init_make_audio_in(self, audio_index):
        """
        make the pvrecorder audio in we will use. Note that
        we can't share one of these between different listeners thanks
        to the .frame_length...

        TODO: could probably super-class interactions with Pico libs?
        """
        audio_in = pvrecorder.PvRecorder(
            self.__rhino.frame_length,
            device_index=audio_index
	)
        self.__audio_in = audio_in

    def interact(self):
        """
        Returns True if feel back to sleep (no commands for awhile)
                False if asked to go back to sleep.
        """
        self.__audio_in.start()
        last_command_time = time.time()
        try:
            while time.time() - last_command_time <= self._SLEEP_AFTER__S:
                audio_frame = self.__audio_in.read()
                is_finalized = self.__rhino.process(audio_frame)

                if is_finalized:
                    inference = self.__rhino.get_inference()
                    if inference.is_understood:
                        log.info("inference=%s", inference)
                        last_command_time = time.time()
                        if inference.intent == 'sleep':
                            return False
                    else:
                        log.info("didn't grok it")
                        # TODO say it outloud.
            log.info("No command in %s seconds. Leaving interaction.", self._SLEEP_AFTER__S)
            return True
        finally:
            self.__audio_in.stop()

    def cleanup(self):
        self.__audio.delete()
        self.__rhino.delete()
