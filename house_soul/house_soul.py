from snore import SleepingDog
from interactor import Interactor
import pvrecorder
import logging

_format_base = "%(asctime)s.%(msecs)03d %(levelname)7s %(threadName)25s %(name)30s::%(funcName)40s:%(lineno)03d %(message)s"
_datefmt_base = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    format=_format_base,
    datefmt=_datefmt_base,
    level=logging.DEBUG
)
log = logging.getLogger(__name__)


class HouseSoul:
    def __init__(self):
        # TODO: config or search for right audio-index...
        log.debug('::Audio-devices::')
        for inx, device in enumerate(pvrecorder.PvRecorder.get_available_devices()):
            log.debug('Device %d: %s', inx, device)
        self.__sleeping_dog = SleepingDog(audio_index=0)
        self.__interactor = Interactor(audio_index=0)

    def run(self):
        try:
            while True:
                keyword = self.__sleeping_dog.wait_to_wake()
                if keyword is None:
                    # TODO: say we died.
                    log.info("Starting exit via dog.")
                    break

                log.info("Has awoken....")
                awake_too_long = self.__interactor.interact()
                if awake_too_long:
                    log.info("Going back to sleep because no command arrived for a long time.")
                else:
                    log.info("Going back to sleep because we were asked to.")
        except KeyboardInterrupt:
            log.info("Stopping")
        finally:
            self.__sleeping_dog.cleanup()


if __name__ == '__main__':
    hs = HouseSoul()
    hs.run()
