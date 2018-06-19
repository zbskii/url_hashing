import unittest
import random
import string
import urlhash

class TestUrlHashing(unittest.TestCase):

    def randstring(self, l=32):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(l)])

    def setUp(self):
        self.hasher = urlhash.UrlHasher()
        random.seed(1415926535) ## Make tests deterministic
        self.urls = []
        for i in range(1000):
            u = "www.%s.com/%s" % (self.randstring(12), self.randstring(32))
            self.urls.append(u)

    def test_hasher(self):
        self.hasher.purge()
        self.hasher.createdirs()
        for u in self.urls:
            h = self.hasher.hash_url(u)
            self.hasher.write_record(h,u)
        for u in self.urls:
            h = self.hasher.hash_url(u)
            self.assertTrue(self.hasher.record_exists(h))
            r = self.hasher.read_record(h)
            self.assertTrue(r[0], u)

    def test_distribution(self):
        hist = {}
        for i in range(2**16):
            u = "www.%s.com/%s" % (self.randstring(12), self.randstring(32))
            h = self.hasher.hash_url(u)
            bucket = h[:4]
            hist[bucket] = hist.setdefault(bucket, 0) + 1
        print "Found %d keys" % len(hist.keys())
        for k, v in hist.items():
            if v == 0:
                print "%s: %s" % (k, v*'*')

