from sys import exit
from exitstatus import ExitStatus
from json import dumps as json_dumps
from getpass import getuser

from px_device_identity.config import get_device_config
from px_device_identity.sign import Sign
from px_device_identity.log import Logger
from px_device_identity.device import Device
from px_device_identity.jwk import JWK
from px_device_identity.classes import RequestedOperation

from .classes import UserClass
from .user import User
from .cli import get_cl_arguments
from .config import KEY_DIR, get_user_config

log = Logger('MAIN')

def handle_result(success):
    if success:
        log.info("We're done here.")
        exit(ExitStatus.success)
    else:
        log.info("Something went wrong.")
        exit(ExitStatus.failure)

def main():
    log.info('------')
    log.info('Welcome to PantherX User Identity Service')
    log.info('------')

    current_user = getuser()
    if current_user == 'root':
        log.warning('!!! To configure root, use px-device-identity on the target device !!!')
        log.warning('!!! Current user: {}'.format(current_user))
        exit()

    cl_arguments = get_cl_arguments()
    operation_class: RequestedOperation = cl_arguments.get('operation')
    user_class: UserClass = cl_arguments.get('user_class')
    message: str = cl_arguments.get('message')
    host: str = cl_arguments.get('host')

    user = User(operation_class, user_class)
    INITIATED = user.check_init()

    if operation_class.action != 'INIT' and INITIATED == False:
        log.error('User is not initiated.')
        log.error('Initiate User with --operation INIT --type <DEFAULT|TPM>')
        exit(ExitStatus.failure)

    try:
        device_config = get_device_config()
    except:
        log.error('Could not read device configuration.')
        log.error('Initiate Device with px-device-identity --operation INIT --type <DEFAULT|TPM>')
        exit(ExitStatus.failure)

    if operation_class.action == 'INIT':
        host = device_config.get('host')
        initiated = user.init(host)
        handle_result(initiated)

    config = get_user_config()
    operation_class.security = config.get('keySecurity')
    operation_class.key_type = config.get('keyType')
    user_class.first_name = config.get('firstName')
    user_class.last_name = config.get('lastName')
    user_class.email = config.get('email')

    # log.info('USER CONFIG')
    # log.info(config)

    if operation_class.action == 'GET_JWK':
        jwk = JWK(operation_class, KEY_DIR())
        return json_dumps(jwk.get())

    if operation_class.action == 'GET_JWKS':
        jwk = JWK(operation_class, KEY_DIR())
        return json_dumps(jwk.get_jwks())

    if operation_class.action == 'SIGN':
        sign = Sign(operation_class, message, KEY_DIR())
        return sign.sign()

if __name__ == '__main__':
    main()