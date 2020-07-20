px-device-identity --operation INIT --security <DEFAULT|TPM> --type <DESKTOP|SERVER|CLOUD|ENTERPRISE> --keytype <RSA:2048|RSA:3072|ECC:p256|ECC:p384|ECC:p521>




if device is managed, user has to be managed



# User Account Registration

The idea is quite simple:

The mobile is the main key, which "signs" everything.
To "authenticate" a user account with the remote device, the user needs to scan the "authentication QR-code".
The user account will then receive a token which it can use to fetch data (for example Accounts) from Central Management.

The token can be revoked.
The user may have accounts on multiple devices.

To login to the device, the user simply scans the QR code. There's no login mask (username, password); simply a QR code field which matches the user phone with the CM account, with the device account.
It could even be possible to live-activate new accounts ("push-accounts"). The user might have to wait 2-3 minutes while the device reconfigures, but then the user account and all settings will be available.
Of course, in order to activate the account, the user still needs to scan the QR code on first login. This is seperate from login!

There are a number of important considerations:
1. People lose their mobile; they should be able to replace it, and login to the same accounts without hassle
2. Maybe there's a better way to bring in user data, without reconfiguring