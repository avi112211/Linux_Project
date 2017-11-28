# Linux_Project

Key generation command line arguments:
./key_gen [key's file]
[key's file] - The wanted file name to save the key.
* Example:
./key_gen key

DES command line arguments:
./des_action [-e/-d] [key file name] [file to enc/dec] [output file]
[-e] for encrypting action.
[-d] for decrypting action.
[key file name] - The file that contains the 64-bit key.
[file to enc/dec] - The wanted file name you would like to encrypt/decrypt.
[output file] - The file name to direct the decrypting/encrypting string into.
* Examples:
./des_action -e key file out_e
./des_action -d key out_e out_d

RSA command line arguments:
(-) ./rsa_action -g [public key file] [private key file]
[public key file] - The file name to save public key into.
[private key file] - The file name to save private key into.
* Example:
./rsa_action -g pub_key pri_key

(-) ./rsa_action [-e/-d] [input file] [output file] [key file]
[-e/-d] - encrypt or decrypt the file provided.
[input file] - The inputted file name to decrypt/encrypt.
[output file] - The output file to save decrypting/encrypting string into.
[key file] - The file name contains key for the decryption/encryption action.
* Examples:
./rsa_action -e key key_e pub_key
./rsa_action -d key_e key_out pri_key

Installation:
perl, switch package for perl, python 2.7, python package wx.
