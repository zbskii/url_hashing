import hashlib
import urlparse
import os.path

TMPDIR="/tmp/urlhasher"

"""
Hash urls into pre-determined partitions
"""

class UrlHasher():

    """
    Generate nice zero padded hex strings with no leading 0x
    """
    def digits(self):
        return [hex(x)[2:].zfill(4) for x in range(65536)]

    """
    Check to see if our hex partitions exist
    """
    def createdirs(self):
        if(not os.path.exists(TMPDIR)):
            os.mkdir(TMPDIR)
            os.chdir(TMPDIR)
        for h in self.digits():
            hashdir = TMPDIR + '/' + h
            if not(os.path.exists(hashdir)):
                os.mkdir(hashdir)

    """
    Entrypoint
    """
    def main(self):
        self.createdirs()
        while True:
            u = raw_input("Enter a url: ")
            result = urlparse.urlparse(u)
            # Somebody input junk
            if (not result[1]):
                print "Bad url!"
                return(0)
            # hash the url
            h = hashlib.sha256(u).hexdigest()
            print "Got hash %s" % h
            # find the diretory
            partf = TMPDIR + '/' + h[:4] + '/' + h
            # See if the url exists, if so print it out
            if os.path.exists(partf):
                print open(partf).readlines()
            else:
                print "File not found in %s saving..." % partf
                fp = open(partf, 'w')
                fp.write(u)
                print "Done!"
