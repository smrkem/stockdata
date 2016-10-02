import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test_is_running(self):
        print("++++++WORKING!!!+++++")
        self.assertEqual(5, 2)


if __name__ == '__main__':
    unittest.main()
