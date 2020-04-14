from .config import Config
from .base import MCConfigurationException


class Remote(object):
    def __init__(self, config=None):
        # if not config.mcurl:
        #     raise MCConfigurationException(
        #         "Remote not properly configured: mcurl is required")
        if config is None:
            config = Config().default_remote
        self.config = config

    def make_url_v2(self, restpath):
        p = self.config.mcurl + '/v2/' + restpath
        return p

    def make_url_v3(self, restpath):
        p = self.config.mcurl + '/v3/' + restpath
        return p

    def make_url_v4(self, restpath):
        p = self.config.mcurl + '/v4/' + restpath
        return p

    def make_url(self, restpath):
        p = self.config.mcurl + "/" + restpath
        return p


class RemoteWithApikey(Remote):
    def __init__(self, apikey, config=Config()):
        if not config.mcurl:
            raise Exception("Remote not properly configured: mcurl is required")

        config.mcapikey = apikey
        self.config = config
