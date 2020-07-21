
import yaml
import shortuuid
from getpass import getuser

from sys import exit
from datetime import datetime
from uuid import uuid4, UUID
from exitstatus import ExitStatus
from string import ascii_uppercase

from px_device_identity.crypto import Crypto
from px_device_identity.filesystem import Filesystem
from px_device_identity.log import Logger
from px_device_identity.jwk import JWK
from px_device_identity.classes import RequestedOperation

from .classes import UserClass
from .config import KEY_DIR, USER_CONFIG_DIR, get_user_config

log = Logger('USER')

class User:
    def __init__(self, operation_class, user_class: UserClass, key_dir = KEY_DIR()):
        self.operation_class = operation_class
        self.security = vars(operation_class)['security'] # DEFAULT / TPM
        self.key_type = vars(operation_class)['key_type']
        self.force_operation = vars(operation_class)['force_operation']
        self.user_type = vars(user_class)['user_type']
        self.is_managed = vars(user_class)['is_managed']
        self.first_name = vars(user_class)['first_name']
        self.last_name = vars(user_class)['last_name']
        self.email = vars(user_class)['email']
        self.username = getuser()
        self.id = str(uuid4())
        self.user_key_dir = key_dir
        self.user_config_dir = USER_CONFIG_DIR()
        self.user_config_path = USER_CONFIG_DIR() + 'user.yml'

    def check_init(self) -> bool:
        try:
            config = get_user_config()
            if len(config.get('id')) == 21:
                log.info('Found Nano ID. Assuming MANAGED user.')
            else:
                try:
                    UUID(config.get('id'), version=4)
                except:
                    return False
            try:
                fs = Filesystem(self.user_key_dir, 'public.pem', 'r')
                public_key = fs.open_file()
                if public_key == False:
                    return False
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
        
    def init(self, host: str) -> True:
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
        
        crypto = Crypto(self.operation_class, self.user_key_dir)
        crypto.generate_and_save_to_key_path()

        # TODO: Get user ID from central management

        config = {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'userType': self.user_type,
            'keySecurity': self.security,
            'keyType': str(self.key_type),
            'isManaged': self.is_managed,
            'host': str(host),
            'configVersion': '0.0.1',
            'initiatedOn': str(datetime.now())
        }

        log.info(config)

        if self.is_managed == True:
            log.info("=> Saving device identification as NanoID in {}".format(self.user_config_path))
        else:
            config['host'] = 'NONE'
            log.info('This user does not belong to any organization (UNMANAGED).')
            log.info("=> Saving user identification as uuid4 in {}".format(self.user_config_path))
            fs = Filesystem(self.user_config_dir, 'user.yml', 'w')
            try:
                fs.create_file(yaml.dump(config))
            except:
                log.error("Could not write user configuration.")
                exit(ExitStatus.failure)
            return True