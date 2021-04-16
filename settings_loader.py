import yaml

from utils import Singleton

TROLL_BOT_CONFIG_FILE = "troll-bot-config.yml"


class Settings:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class SettingLoader(Singleton):

    def __init__(self):
        if not self.loaded:
            self._settings = self.load_settings()
            self.loaded = True

    @property
    def loaded(self):
        if hasattr(self, '_loaded'):
            return self._loaded
        return False

    @loaded.setter
    def loaded(self, value):
        self._loaded = value

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @staticmethod
    def load_settings():
        with open(TROLL_BOT_CONFIG_FILE, 'r') as stream:
            try:
                print("Load settings file")
                setting_dict = yaml.safe_load(stream)
                settings = Settings(**setting_dict)
                return settings
            except yaml.YAMLError as exc:
                print(exc)
