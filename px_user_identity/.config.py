import yaml
from pathlib import Path

from .log import Logger
from .filesystem import Filesystem

log = Logger('CONFIG')

def KEY_DIR():
    home_path = str(Path.home())
    key_dir = '/.ssh/'
    return home_path + key_dir

def USER_CONFIG_DIR():
    home_path = str(Path.home())
    config_dir = '/.config/px-device-identity/'
    return home_path + config_dir

def get_user_config():
    log.info('Loading user config from {}.'.format(USER_CONFIG_DIR()))
    fs = Filesystem(CONFIG_DIR(), 'user.yml', 'r')
    file = fs.open_file()
    config = yaml.load(file, Loader=yaml.BaseLoader)
    cfg_user = {
        'id': config.get('id'),
        'userType': config.get('userType'),
        'keySecurity': config.get('keySecurity'),
        'keyType': config.get('keyType'),
        'isManaged': config.get('isManaged'),
        'host': config.get('host'),
        'configVersion': config.get('configVersion'),
        'initiatedOn': config.get('initiatedOn')
    }
    return cfg_user

