import argparse
from sys import exit
from exitstatus import ExitStatus

from px_device_identity.log import Logger
from px_device_identity.classes import RequestedOperation
from .classes import UserClass

log = Logger('CLI')

def get_cl_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str, required=True,
        choices=['INIT', 'SIGN', 'GET_JWK', 'GET_JWKS'],
        help="Primary operations.")
    parser.add_argument("-fn", "--firstname", type=str, default='NONE',
        help="User first name (INIT only)")
    parser.add_argument("-ln", "--lastname", type=str, default='NONE',
        help="User last name (INIT only)")
    parser.add_argument("-em", "--email", type=str, default='NONE',
        help="User email address")
    parser.add_argument("-s", "--security", type=str, default='TPM',
        choices=['DEFAULT', 'TPM'],
        help="Operating types: On supported hardware, the usage of TPM is encouraged.")
    parser.add_argument("-k", "--keytype", required=False, default='ECC:p256',
        choices=['RSA:2048', 'RSA:3072', 'ECC:p256','ECC:p384', 'ECC:p521'],
        help="Key type and relative strength RSA:BITS / ECC:curve.")
    parser.add_argument("-t", "--type", type=str, default='STANDALONE',
        choices=['STANDALONE', 'DESKTOP', 'APPLICATION'],
        help="User type. Defaults to STANDALONE.")
    parser.add_argument("-m", "--message", type=str,
        help="Pass message to SIGN operation")
    parser.add_argument("-f", "--force", type=bool, default=False,
        choices=[True, False],
        help="Force operations: Overwrite existing user identity. Use with caution!")
    parser.add_argument("-d", "--debug", type=bool, default=False,
        help="Turn on debug messages")
    args = parser.parse_args()

    is_managed = False
    user_type = args.type
    first_name = args.firstname
    last_name = args.lastname
    email = args.email
    if args.operation == 'INIT':
        if args.security is None:
            log.error("You need to indicate the key security with --security <DEFAULT|TPM>.")
            exit(ExitStatus.failure)
        if args.firstname == 'NONE':
            log.error("You need to indicate the user first name with --firstname")
            exit(ExitStatus.failure)
        if args.lastname == 'NONE':
            log.error("You need to indicate the user last name with --lastname")
            exit(ExitStatus.failure)
        if args.email == 'NONE':
            log.error("You need to indicate the user email address with --email")
            exit(ExitStatus.failure)
            
    if args.operation == 'SIGN':
        if args.message is None:
            log.error("You need to pass a --message for signing.")
            exit(ExitStatus.failure)

    operation_class = RequestedOperation(args.operation, args.security, args.keytype, args.force)
    user_class = UserClass('', user_type, is_managed, first_name, last_name, email)

    return {
        'operation': operation_class, # RequestedOperation
        'user_class': user_class,
        'message': args.message,
        'debug': args.debug
    }