#!/usr/bin/env python3
import unittest
import menu
import random

rand=random.randrange(1000)

class Tests(unittest.TestCase):

    def setUp(self):
        menu.app.testing = True
        self.app = menu.app.test_client()
        

    def test_home(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(bytearray("Welcome,", 'utf-8'), rv.data)

    def test_get(self):
        rv = self.app.get('/get')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(bytearray("GigabitEthernet1", 'utf-8'), rv.data)

    def test_add(self):
        global rand
        rv = self.app.get(f'/add/{rand}/test/10.0.0.10/255.255.255.0')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(bytearray(f"{rand}", 'utf-8'), self.app.get('/get').data)

    def test_del(self):
        global rand
        rv = self.app.get(f'/del/{rand}')
        self.assertEqual(rv.status, '200 OK')
        self.assertFalse(bytearray(f"Loopback{rand}", 'utf-8') in self.app.get('/get').data)
        


if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
