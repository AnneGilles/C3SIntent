#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# you need python-gnupg, so
# bin/pip install python-gnupg

import gnupg
import tempfile
import shutil

DEBUG = False
#DEBUG = True


def encrypt_with_gnupg(data):

    # we use a folder named 'keys' to store stuff

#    if os.path.exists("keys"):
#        if DEBUG:  # pragma: no cover
#            print("===================================== GNUPG START")
#            print "folder 'keys' exists"
        # shutil.rmtree("keys")     # delete to renew
        # print "deleted keys"

    # tempfile approach
    keyfolder = tempfile.mkdtemp()
#    print(keyfolder)
# TODO: check for a better way to do this:
# do we really need to create a new tempdir for every run? no!
# but hey as long as we neet to run both as 'normal' user (while testing
# on port 6544) and as www-data (apache) we do need separate folders,
# because only the creator may access it.
# however: as long as this is reasonably fast, we can live with it. for now...

#    if DEBUG:  # pragma: no cover
#        # a gpg object to work with
#        gpg = gnupg.GPG(gnupghome="keys", verbose=True)
#    else:
        #gpg = gnupg.GPG(gnupghome="keys")
    gpg = gnupg.GPG(gnupghome=keyfolder)
    gpg.encoding = 'utf-8'

    # check if we have the membership key
    list_of_keys = gpg.list_keys()
    if DEBUG:  # pragma: no cover
        print("=== the list of keys: " + repr(list_of_keys))

    if not 'C3S-Yes!' in str(list_of_keys):
        # open and read key file
        # reading public key
#        pubkey_file = open('keys/C3S-Yes!.asc', 'r')
#        pubkey_content = pubkey_file.read()
#        pubkey_file.close()

        pubkey_content = """
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.11 (GNU/Linux)

mQENBFBIqlMBCADR7hxvDnwJkLgXU3Xol71eRkdNCAdIDnXQq/+Bmn5rxcJcXzNK
DyibSGbVVpwMMOIiVuKxM66QdlvBm+2/QUdD/kdcMTwRBFqP40N9T+vaIVDpit4r
6ZH1w8QD6EJTL0wbtmIkdAYMhYd0k4wDJ+xOcfx/VINiwhS5/DT38jimqmkaOEzs
DqzbBBogdZ+Tw+leC+D9JkSzGRjwO+UzUxjw4kdib9KbSppTbjv7HdL+Pn1y0ACd
2ELZjTumqQzQi19WFENNhMaRHlUU5iGp9sLbKUN0GtgxGYIs85QNXH/5/0Qr2ZjH
2/yZCyyWzZR0efut6WthcxFNb4OMDs056v5LABEBAAG0KUMzUyBZZXMhIChodHRw
Oi8vd3d3LmMzcy5jYykgPHllc0BjM3MuY2M+iQE+BBMBAgAoBQJQSKpTAhsDBQkB
4TOABgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRBx9rqRzdKBECXRCADA+HuD
D6qoyMHBpsf8vuVyQfsORyuTfTe+Pv35WbsgPGtFpPmLXKaWbGRuCYl/FSOkd/ws
VzucQNUhHmZGnmbtMv24+eyPPjbOGzG66DLSKcmL64Eaev23k7tCfpUK8pLB38ub
FRoZ8PY2oSzkybQqRnqCN1rCRzXqOCsqXts+WqTmOR5s+o5VSisEtiaekBcPkV3H
3bGut6yIh9fwSw6RoKsjhdUgXz94wxS+3K8BDmo28rsfPuBcc0YqWk2Dm9jo3L9v
fASXB277bE60RGJlBvOpM23ArxfbCaXEyq5GUtmaZLqgPy021QSikHeG0rreeA8x
b7g+mAsuVH08eYnBuQENBFBIqlMBCACoys54nxs3nrRcUkwFG0lp3L8N0udCzckI
iVgU/1SdgbfAD9rnRdKv4UE/uvn7MkfyO8V2V2OZANu8ZL+dtjmi6DWS2iTEXOl6
Mn6j0FyvZNDe6scvahPDjWYnrjOwrNy6FC5Y4eAyHTprABioZgfwNkonK5Oh0pXL
Rkr5z00lHjnkxYwyoFoMa3T7j7sxS0t3bkYZxETMCd+5YqDyt7fPEZ2sPugi1oqV
U/ytADNgEpjkzUhl4iWYYkk8RlQ8MFWVWEJd34HO6iOT+Pz6A9anuRbEqYCWYlHx
M3wBc2Klv/heN0yz5ldZVx1ug0/eLwexNecJOTpy2eQYjVLP/BwTABEBAAGJASUE
GAECAA8FAlBIqlMCGwwFCQHhM4AACgkQcfa6kc3SgRBoPQgAx/73uYoQfqFrfCDd
HRnzf2r3CyMOMYpmHmzVQjqsvVWUc59g1xpxG25CFYRTvC2OpJFP+yLsW52TbJjQ
PYKdzV4zmjDJPb9msu4Bztrg+lZEpovqSF4Au9Jii7DbE1TQ8zItMzTGvC0deP4+
SY27efmf3PHSXS4TIQxas5d+Y0sa3RyiE0E97uK7akJMDDS6l3t0YWaOfXhtknNV
aGvLiYsbGr6JUEtnpCo0TawHtkxFy7L3bi9CF2dSF0oOzQWXh/LjLeiosh/oL7ce
TN71vKWaPJFWl5pXxsEUGCdq2UUTRviHNx2+lzzdOmYBL+kaoHC5C50NuahZ4KAh
BxTGRw==
=ZhQb
-----END PGP PUBLIC KEY BLOCK-----
"""

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
        '89FC70ECCAD4487972D8924D71F6BA91CDD28110',  # key fingerprint
        always_trust=True)

    #print "encrypted: " + str(encrypted)
    #print "len(encrypted): " + str(len(str(encrypted)))
    if DEBUG:  # pragma: no cover
        print ("========================================== GNUPG END")
    shutil.rmtree(keyfolder)
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
