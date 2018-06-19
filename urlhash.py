import hashlib
import urlparse
import os.path
import shutil

TMPDIR="/tmp/urlhasher"

"""
Partition a set of urls across pre-defined partitions.  The example
here simply uses urls, but could be extended to arbitrary records of
data.
"""

class UrlHasher():

    """
    Generate nice zero padded hex strings with no leading 0x
    """
    def digits(self):
        return [hex(x)[2:].zfill(4) for x in range(2**16)]

    def createdirs(self):
        """
        Check to see if our hex partitions exist
        """
        if(not os.path.exists(TMPDIR)):
            os.mkdir(TMPDIR)
            os.chdir(TMPDIR)
        for h in self.digits():
            hashdir = TMPDIR + '/' + h
            if not(os.path.exists(hashdir)):
                os.mkdir(hashdir)

    """
    partition utility functions
    """
    def hash_url(self, u):
        return hashlib.sha256(u).hexdigest()

    def get_file(self, h):
        return TMPDIR + '/' + h[:4] + '/' + h

    def parse_url(self, u):
        return urlparse.urlparse(u)

    def record_exists(self, h):
         return os.path.exists(self.get_file(h))

    def read_record(self, h):
        if not self.record_exists(h):
            return False
        return open(self.get_file(h)).readlines()

    def write_record(self, h, u):
        partf = self.get_file(h)
        with open(partf, 'w') as fp:
            fp.write(u)
            fp.flush()

    def purge(self):
        if(os.path.exists(TMPDIR)):
            shutil.rmtree(TMPDIR)

    """
    Entrypoint
    """
    def main(self):
        self.createdirs()
        while True:
            u = raw_input("Enter a url: ")
            result = self.parse_url(u)

            # Somebody input junk
            if (not result[1]):
                print "Bad url!"
                return(0)

            # hash the url
            h = self.hash_url(u)
            print "Got hash %s" % h

            # find the diretory
            partf = TMPDIR + '/' + h[:4] + '/' + h
            # See if the url exists, if so print it out
            if self.record_exists(h):
                print self.read_record(h)
            else:
                print "File not found in %s saving..." % partf
                self.write_record(h, u)
                print "Done!"
