
import yaml
import shortuuid

from sys import exit
from datetime import datetime
from uuid import uuid4, UUID
from exitstatus import ExitStatus
from string import ascii_uppercase

from .classes import DeviceClass, RequestedOperation
from px_device_identity.crypto import Crypto
from px_device_identity.filesystem import Filesystem
from px_device_identity.log import Logger
from .cm import CM
from px_device_identity.jwk import JWK
from .config import KEY_DIR, USER_CONFIG_DIR, get_user_config

log = Logger('USER')

class User:
    def __init__(self, operation_class, user_class: UserClass, key_dir = KEY_DIR()):
        self.operation_class = operation_class
        self.security = operation_class.security
        self.key_type = vars(operation_class)['key_type']
        self.user_type = vars(user_class)['user_type']
        self.user_is_managed = vars(user_class)['user_is_managed']
        self.force_operation = vars(operation_class)['force_operation']
        self.id = uuid4()
        self.user_key_dir = key_dir
        self.user_config_dir = USER_CONFIG_DIR()
        self.user_config_path = USER_CONFIG_DIR() + 'user.yml'

    def check_init(self) -> bool:
        try:
            config = get_user_config()
            if len(config.get('id')) == 21:
                log.info('Found Nano ID. Assuming MANAGED user.')
            else:
                UUID(config.get('id'), version=4)
            try:
                public_key_path = self.user_key_dir + 'public.pem'
                with open(public_key_path) as public_key_reader:
                    public_key_reader.read()
                return True
            except FileNotFoundError:
                return False
        except FileNotFoundError:
            return False

    def check_is_managed(self):
        log.info('=> Verifying whether user is part of an organization (MANAGED).')
        try:
            config = get_user_config()
            is_managed = config.get('isManaged')
            host = config.get('host')
            if host != 'NONE' and is_managed == True:
                return True
        except:
            log.error('Could not read config file at {}'.format(self.user_config_path))
        return False
        
    def init(self, host: str):
        if self.check_init():
            if self.force_operation:
                log.warning('User has already been initiated.')
                log.warning("=> FORCE OVERWRITE")
            else:
                log.error('User has already been initiated.')
                log.error("Use '--force True' to overwrite. Use with caution!")
                exit(ExitStatus.failure)
        else:
            log.info("=> Initiating a new user identity")
            fs = Filesystem(USER_CONFIG_DIR(), 'none', 'none')
            fs.create_path()
        
        crypto = Crypto(self.operation_class)
        crypto.generate_and_save_to_key_path()

        # TODO: Get user ID from central management

        device_id_str = str(UUID(version=4))
        config = {
            'id': device_id_str,
            'email': 
            'deviceType': self.user_type,
            'keySecurity': self.security,
            'keyType': str(self.key_type),
            'isManaged': self.user_is_managed,
            'host': str(host),
            'configVersion': '0.0.1',
            'initiatedOn': str(datetime.now())
        }

        if self.user_is_managed == True:
            log.info("=> Saving device identification as NanoID in {}".format(self.user_config_path))
        else:
            config['host'] = 'NONE'
            log.info('This user does not belong to any organization (UNMANAGED).')
            log.info("=> Saving user identification as uuid4 in {}".format(self.user_config_path))

        try:
            with open(self.user_config_path, 'w') as fs_device_writer:
                fs_device_writer.write(yaml.dump(config))
        except:
            log.error("Could not write user configuration.")
            return False
        return True
