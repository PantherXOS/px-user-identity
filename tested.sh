#!/bin/sh
# PantherX User Identity regularly tested features
# Version 0.0.4
# Author: Franz Geffke <franz@pantherx.org> | PantherX.DEV

PROGNAME=$(basename $0)

error_exit()
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

function common {
    px-user-identity --operation GET_JWK || error_exit
    echo ""
    px-user-identity --operation GET_JWKS || error_exit
    echo ""
    px-user-identity --operation SIGN --message ABC || error_exit
    echo ""
}

function common_tpm {
    px-user-identity --operation GET_JWK || error_exit
    echo ""
    px-user-identity --operation GET_JWKS || error_exit
    echo ""
    px-user-identity --operation SIGN --message ABC || error_exit
    echo ""
}

echo "###################"
echo "Test 1: Default"
px-user-identity --operation INIT --security DEFAULT --type STANDALONE --keytype RSA:2048 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common
echo ""
echo "###################"
echo "Test 2: Default with TPM"
px-user-identity --operation INIT --security TPM --type STANDALONE  --keytype RSA:2048 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common_tpm
echo ""
echo "###################"
echo "Test 3: ECC"
px-user-identity --operation INIT --security DEFAULT --type STANDALONE --keytype ECC:p256 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common
px-user-identity --operation INIT --security DEFAULT --type STANDALONE --keytype ECC:p384 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common
px-user-identity --operation INIT --security DEFAULT --type STANDALONE --keytype ECC:p521 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common
echo ""
echo "###################"
echo "Test 3: ECC with TPM"
px-user-identity --operation INIT --security TPM --type STANDALONE --keytype ECC:p256 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common_tpm
px-user-identity --operation INIT --security TPM --type STANDALONE --keytype ECC:p384 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common_tpm
px-user-identity --operation INIT --security TPM --type STANDALONE --keytype ECC:p521 --force True --firstname Franz --lastname Geffke --email franz@pantherx.org
common_tpm