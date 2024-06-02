import yaml
from yaml import SafeLoader


class Config:
    def __init__(self) -> None:
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file, SafeLoader)
            self.TOKEN = config['TOKEN']
            self.command_prefix = config['command_prefix']
            self.tracks_dir = config['tracks_dir']