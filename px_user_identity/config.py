import yaml
from pathlib import Path

from px_device_identity.log import Logger
from px_device_identity.filesystem import Filesystem

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
    log.info('=> Loading user config from {}.'.format(USER_CONFIG_DIR()))
    fs = Filesystem(USER_CONFIG_DIR(), 'user.yml', 'r')
    file = fs.open_file()
    config = yaml.load(file, Loader=yaml.BaseLoader)
    cfg_user = {
        'id': config.get('id'),
        'first_name': config.get('firstName'),
        'last_name': config.get('lastName'),
        'email': config.get('email'),
        'userType': config.get('userType'),
        'keySecurity': config.get('keySecurity'),
        'keyType': config.get('keyType'),
        'isManaged': config.get('isManaged'),
        'configVersion': config.get('configVersion'),
        'initiatedOn': config.get('initiatedOn')
    }
    return cfg_user

