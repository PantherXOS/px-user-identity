# PantherX User Identity Manager

- Generates ECC/RSA keypair and user configuration
- Generates and saves JWK from public key

### Supported cryptography

**RSA** with
- 2048 bits `RSA:2048`
- 3072 bits `RSA:3072`

**ECC** with
- p256 curve `ECC:p256`
- p384 curve `ECC:p384`
- p521 curve `ECC:p521`

All supported options work for both file-based and TPM2-based key-pairs.

### Supported devices

File-based keys should work everywhere but we specifically test TPM2-support on the following devices:

- ThinkPad T450, X1CG7
- ThinkStation M625q

## Setup

**Requirements**

- `openssl`
- [`tpm2-tss-engine`](https://github.com/tpm2-software/tpm2-tss-engine)

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .
```

## Run

### Initiate user:

Overview of user types:

- `STANDALONE`: Single user (home user)
- `DESKTOP`: User on a company network (MANAGED)
- `APPLICATION`: Application on a company network (SERVER, MANAGED)

**Unmanaged**

Defaults to _type_ `STANDALONE`:

```bash
$ px-user-identity --operation INIT --security <DEFAULT|TPM> --firstname <FIRST_NAME> --lastname <LAST_NAME> --email <EMAIL>
```

All options:

```bash
$ px-user-identity --operation INIT --security <DEFAULT|TPM> --type <STANDALONE|DESKTOP|APPLICATION> --keytype <RSA:2048|RSA:3072|ECC:p256|ECC:p384|ECC:p521> --firstname <FIRST_NAME> --lastname <LAST_NAME> --email <EMAIL>
```

A good default for user without TPM2 support is:

```bash
$ px-user-identity --operation INIT --security DEFAULT --type <STANDALONE|DESKTOP|APPLICATION> --keytype ECC:p256 --firstname <FIRST_NAME> --lastname <LAST_NAME> --email <EMAIL>
```

**Managed**

Defaults to _type_ `DESKTOP`:

```bash
$ px-user-identity --operation INIT --security <DEFAULT|TPM> --type <DESKTOP|APPLICATION> --firstname <FIRST_NAME> --lastname <LAST_NAME> --email <EMAIL>
```

- `DEFAULT` - private key stored as PEM file
- `TPM` - private key stored in TPM2

This generates the following files:

```bash
~/.config/user/user.yml
~/.ssh/public.pem
~/.ssh/private.pem
```

The `user.yml` contains the user configuration:

```yml
id: str # ['UUID4', 'NanoID']
firstName: str
lastName: str
email: str
userType: str # ['STANDALONE', 'DESKTOP', 'ENTERPRISE']
keySecurity: str # ['DEFAULT', 'TPM']
keyType: str # ['RSA:bitrate', 'ECDSA:curve']
isManaged: bool # [true, false]
configVersion: str # ['*.*.*']
initiatedOn: dateTime # ['2020-07-03 23:02:36.733746']
```

Here's an example for an unmanaged user (basically a home user):

```yml
configVersion: 0.0.1
email: franz@pantherx.org
firstName: Franz
id: 1c0ab587-07ca-4c14-9fdf-ba98804361c9
initiatedOn: '2020-07-21 21:40:44.813347'
isManaged: false
keySecurity: TPM
keyType: ECC:p256
lastName: Geffke
userType: STANDALONE
```

**To overwrite an existing device identification**, do:

```bash
px-user-identity --operation INIT --security <DEFAULT|TPM> --force TRUE
```

### Get the JWK for the user public key

```bash
px-user-identity --operation GET_JWK
```

### Get the JWK as JWKS

```bash
px-user-identity --operation GET_JWKS
```

### Sign a hash

```bash
px-user-identity --operation SIGN --message <MESSAGE>
```

returns `base64`

#### Example for JWT

Request signature:

```bash
px-user-identity --operation SIGN --message eyJhbGciOiAiUlMyNTYiLCAidHlwZSI6ICJKV1QifQ.eyJhcHBfaWQiOiAiYzNlZmMzYTYtZGE1MS00N2IwLWFiNTYtOTA4MjRkYTFmNDNmIn0
```

Response:

```bash
UWyxzPn_r9VAdKH0MKwHirI3saCn21IuHpYNxMMgzq0KQk1PK83MBYTxqhnEwpq17ruKwQehhXb5bPg4Z9XF6a_dotdyZ8gYlrOefyBPBD712k0gPFOmf0KtJn6jYaR10lPbRyKI-fo21sb-0COp7Sb62rwNPv43tABiFD5C7mltYlH2EF2lN58uDytQypUCToWSapcRgfO9L5NCGShsjubBKkoLjzrP4qPC-AB8-EQx8jCm2hzy0dPg0GtppG1ZnLzeB0g2Vt4dFH21bjVO4o97CNb95PP6pZhNdqOq5LjsTfS6CbFi3h5bXHQQN_VU2mjq_E_5_QDeH8SAAFW-2g
```

### Misc

To output to a file, simply

```bash
> jwk.json
```

# Next

## User Account Registration

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