#!/usr/bin/env python
import hashlib
import urlparse
import os.path

TMPDIR="/tmp/urlhasher"

"""
Generate nice zero padded hex strings with no leading 0x
"""
def digits():
    return [hex(x)[2:].zfill(4) for x in range(65536)]

"""
Check to see if our hex partitions exist
"""
def createdirs():
    if(not os.path.exists(TMPDIR)):
        os.mkdir(TMPDIR)
    os.chdir(TMPDIR)
    for h in digits():
        if not(os.path.exists(h)):
            os.mkdir(TMPDIR + '/' + h)

"""
Entrypoint
"""
def main():
    createdirs()
    while True:
        u = raw_input("Enter a url: ")
        result = urlparse.urlparse(u)
        # Somebody input junk
        if (not result[1]):
            print "Bad url!"
            return(0)
        # hash the url
        h = hashlib.sha256(u).hexdigest()
        # find the diretory
        uf = TMPDIR + '/' + h[:4]
        # See if the url exists, if so print it out
        if os.path.exists(uf):
            print open(uf).readlines()
        else:
            print "File not found in %s saving..." % uf
            fp = open(uf, 'w')
            fp.write(u)
            print "Done!"

if __name__ == "__main__":
    exit(main())
