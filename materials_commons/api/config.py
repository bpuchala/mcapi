import getpass
import os
import warnings
from os.path import join
import json
from .base import MCConfigurationException

class RemoteConfig(object):
    def __init__(self, mcurl=None, email=None, mcapikey=None):
        self.mcurl = mcurl
        self.email = email
        self.mcapikey = mcapikey

    def __eq__(self, other):
        """Equal if mcurl and email are equal, does not check mcapikey"""
        return self.mcurl == other.mcurl and self.email == other.email

    def get_params(self):
        return {'apikey': self.mcapikey}

class GlobusConfig(object):
    def __init__(self, transfer_rt=None):
        self.transfer_rt = transfer_rt

class InterfaceConfig(object):
    def __init__(self, name=None, module=None, subcommand=None, desc=None):
        self.name = name
        self.module = module
        self.subcommand = subcommand
        self.desc = desc

    def __eq__(self, other):
        return vars(self) == vars(other)


class Config(object):
    """Configuration variables

    Order of precedence:
        1. override_config, variables set at runtime
        2. environment variables
        3. configuration file
        4. default configuration

    Format:
        {
            "default_remote": {
              "mcurl": <url>,
              "email": <email>,
              "apikey": <apikey>
            },
            "remotes": [
                {
                    "mcurl": <url>,
                    "email": <email>,
                    "apikey": <apikey>
                },
                ...
            ],
            "interfaces": [
                {   'name': 'casm',
                    'desc':'Create CASM samples, processes, measurements, etc.',
                    'subcommand':'casm_subcommand',
                    'module':'casm_mcapi'
                },
                ...
            ],
            "globus": {
                "transfer_rt": <token>
            },
            "developer_mode": False,
            "REST_logging": False,
            "mcurl": <url>, # (deprecated) use if no 'default_remote'
            "apikey": <apikey> # (deprecated) use if no 'default_remote'
        }

    Attributes:
        remotes: Dict of RemoteConfig, mapping of remote name to RemoteConfig instance
        default_remote: RemoteConfig, configuration for default Remote
        interfaces: List of InterfaceConfig, settings for software interfaces for the `mc` CLI program
        globus: GlobusConfig, globus configuration settings

    Arguments:
        config_file_path: str, path to config directory. Defaults to ~/.materialscommons.
        config_file_name: str, name of config file. Defaults to "config.json".
        override_config: dict, config file-like dict, with settings to use instead of those in
            environment variables or the config file. Defaults to {}.
    """

    def __init__(self, config_file_path=None, config_file_name="config.json", override_config={}):

        # generate config file path
        if not config_file_path:
            user = getpass.getuser()
            config_file_path = join(os.path.expanduser('~' + user), '.materialscommons')
        self.config_file = join(config_file_path, config_file_name)

        # read config file, or use default config
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        else:
            # default config
            config = {
                'apikey': None,
                'mcurl': None,
                'remotes': {},
                'interfaces': {},
                'globus': {}
            }

        # check for recognized environment variables
        env_apikey = os.environ.get("MC_API_KEY")
        env_mcurl = os.environ.get("MC_API_URL")

        if env_apikey:
            config['apikey'] = env_apikey
        if env_mcurl:
            config['mcurl'] = env_mcurl

        # override with runtime config
        for key in override_config:
            config[key] = override_config[key]

        # handle deprecated 'mcurl' and 'apikey'
        if config.get('mcurl') and config.get('apikey') and 'default_remote' not in config:
            config['default_remote'] = {
                'mcurl': config.get('mcurl'),
                'email': '__default__',
                'mcapikey': config.get('apikey')
            }

        self.remotes = [RemoteConfig(**kwargs) for kwargs in config.get('remotes',[])]
        self.default_remote = RemoteConfig(**config.get('default_remote',{}))

        self.interfaces = [InterfaceConfig(**kwargs) for kwargs in config.get('interfaces',[])]

        self.globus = GlobusConfig(**config.get('globus'))

        self.developer_mode = config.get('developer_mode', False)
        self.REST_logging = config.get('REST_logging', False)

    def save(self):
        config = {
            'default_remote': vars(self.default_remote),
            'remotes': [vars(value) for value in self.remotes],
            'globus': vars(self.globus),
            'interfaces': [vars(value) for value in self.interfaces],
            'developer_mode': self.developer_mode,
            'REST_logging': self.REST_logging
        }
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(config, indent=2))
