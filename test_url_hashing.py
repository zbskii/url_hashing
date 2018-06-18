import unittest
import random
import string
import urlhash

class TestUrlHashing(unittest.TestCase):

    def randstring(self, l=32):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(l)])

    def setUp(self):
        self.hasher = urlhash.UrlHasher()
        self.hasher.createdirs()
        random.seed(1415926535)
        self.urls = []
        for i in range(1000):
            u = "www.%s.com/%s" % (self.randstring(12), self.randstring(32))
            self.urls.append(u)


    def test_hasher(self):
        for u in self.urls:
            self.hasher.hash_url(u)
