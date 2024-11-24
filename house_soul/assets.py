from pathlib import Path
from logging import getLogger

log = getLogger(__name__)


class AssetAccess:
    def __init__(self, globber):
        self.__assets_root = Path(__file__).parent / "assets"
        self.__globber = globber
        self.__file_data = None
        log.debug("asset %s, root=%s, globber=%s", self, self.__assets_root,
                  self.__globber)

    def __build_file_data(self):
        if self.__file_data is not None:
            return

        file_data = {}
        for a_matched_path in self.__assets_root.glob(self.__globber):
            stem_name = a_matched_path.stem
            keyword = self._stem_name_to_keyword(stem_name)
            assert keyword not in file_data, \
                'duplicate keyword {} from {}. Other was from {}'.format(
                    keyword, stem_name, file_data[keyword])
            file_data[keyword] = a_matched_path.as_posix()
        self.__file_data = file_data

    def _stem_name_to_keyword(self, stem_name):
        return stem_name

    def get_file_list(self):
        self.__build_file_data()
        return list(self.__file_data.values())

    def get_keyword_list(self):
        self.__build_file_data()
        return list(self.__file_data.keys())

    def get_keyword_and_file_lists(self):
        kl = self.get_keyword_list()
        fl = self.get_file_list()
        return kl, fl


class PicoAsset(AssetAccess):
    def __init__(self, suffix):
        super().__init__('*.{}'.format(suffix))

    def _stem_name_to_keyword(self, stem_name):
        """
        Pico seems to use the same general format for their files:
        the_actual_name_of_the_thing_raspberry-pi_v3_0_0.suffix.

        They have a sketchy file-name to "keyword" chunk of code that
        kind of presumes this. Stealing for here until there is a reason
        for something smarter.
        """
        keyword_phrase_part = stem_name.split('_')
        if len(keyword_phrase_part) > 6:
            keyword = ' '.join(keyword_phrase_part[0:-6])
        else:
            keyword = keyword_phrase_part[0]

        return keyword

    
class PorcupineWakeAssets(PicoAsset):
    def __init__(self):
        super().__init__("ppn")


class RhinoContextAssets(PicoAsset):
    def __init__(self):
        super().__init__("rhn")
