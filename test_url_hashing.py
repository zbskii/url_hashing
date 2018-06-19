import collections
import random
import string
import unittest
import urlhash
import sys

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
        random.seed() ## We want to test the distribution
        hist = {b: 0 for b in self.hasher.digits()}
        for i in range(2**20):
            if not i % 10000:
                sys.stdout.write('.')
            u = "www.%s.com/%s" % (self.randstring(12), self.randstring(32))
            h = self.hasher.hash_url(u)
            bucket = h[:4]
            hist[bucket] += 1
        vals = collections.Counter(hist.values())
        print "Key distribution histogram"
        for n,c in sorted(vals.items()):
            print "%s: %s" % (n, c)

