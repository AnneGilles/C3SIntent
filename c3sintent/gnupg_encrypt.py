#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# you need python-gnupg, so
# bin/pip install python-gnupg

import gnupg
import os
#import shutil

DEBUG = False


def encrypt_with_gnupg(data):

    # we use a folder named 'keys' to store stuff

    if os.path.exists("keys"):
        if DEBUG:  # pragma: no cover
            print("===================================== GNUPG START")
            print "folder 'keys' exists"
        # shutil.rmtree("keys")     # delete to renew
        # print "deleted keys"

    if DEBUG:  # pragma: no cover
        # a gpg object to work with
        gpg = gnupg.GPG(gnupghome="keys", verbose=True)
    else:
        gpg = gnupg.GPG(gnupghome="keys")

    # check if we have the membership key
    list_of_keys = gpg.list_keys()
    if DEBUG:  # pragma: no cover
        print("=== the list of keys: " + repr(list_of_keys))

    if not 'C3S-Yes!' in str(list_of_keys):
        # open and read key file
        # reading public key
        pubkey_file = open('keys/C3S-Yes!.asc', 'r')
        pubkey_content = pubkey_file.read()
        pubkey_file.close()

        # import public key
        gpg.import_keys(pubkey_content)
    else:
        if DEBUG:  # pragma: no cover
            print("=== not imported: key already known")
        pass

    if DEBUG:  # pragma: no cover
        print "list_keys(): " + str(gpg.list_keys())

    # prepare
    #to_encode = unicode(data, gpg.encoding)
    to_encode = data
    to_encrypt = to_encode.encode(gpg.encoding)
    if DEBUG:  # pragma: no cover
        print "len(to_encrypt): " + str(len(str(to_encrypt)))

    # encrypt
    encrypted = gpg.encrypt(
        to_encrypt,
        '89FC70ECCAD4487972D8924D71F6BA91CDD28110',
        always_trust=True)

    #print "encrypted: " + str(encrypted)
    #print "len(encrypted): " + str(len(str(encrypted)))
    if DEBUG:  # pragma: no cover
        print ("========================================== GNUPG END")
    return encrypted


if __name__ == '__main__':  # pragma: no coverage

    my_text = """
    --                                      --
    --  So here is some sample text.        --
    --  I want this to be encrypted.        --
    --  And then maybe send it via email    --
    --                                      --
    """
    result = encrypt_with_gnupg(my_text)
    print result
