import unittest

from virtual_modi.virtual_bundle import VirtualBundle


class TestVirtualBundle(unittest.TestCase):

    def setUp(self):
        self.vb = VirtualBundle()
        self.vb.open()

    def tearDown(self):
        self.vb.close()

    def test_init(self):
        self.assertEqual(self.vb.conn_type, 'ser')


if __name__ == "__main__":
    unittest.main()