import unittest

from app.checkers.user import register_params_check


class BasicTestCase(unittest.TestCase):
    '''
    TODO: 在这里补充注册相关测试用例
    '''
    # correct
    test1 = {
        'username': "a2322002",
        'password': "6018As00_",
        'nickname': "gw",
        'url': "http://192.23.4s2",
        'mobile': "+86.123482974401",
        'magic_number': 12
    }
    # lack username 
    test2 = {
    }
    # lack password
    test3 = {
        'username': "a2322002",
    }
    # lack nickname
    test4 = {
        'username': "a2322002",
        'password': "6018As*00"
    }
    # lack url
    test5 = {
        'username': "a2322002",
        'password': "6018As00_",
        'nickname': "gw",
    }
    # lack mobile
    test6 = {
        'username': "a2322002",
        'password': "6018As00_",
        'nickname': "gw",
        'url': "http://192.23.4s2",
    }
    # lack magic_number
    test7 = {
        'username': "a2322002",
        'password': "6018As00_",
        'nickname': "gw",
        'url': "http://192.23.4s2",
        'mobile': "+86.123482974401",
    }
    # wrong username
    test8 = {
        'username': "2322002",
    }
    test9 = {
        'username': "23"
    }
    # wrong password
    test10 = {
        'username': "a2322002",
        'password': "60?18Aa-",
    }
    test11 = {
        'username': "a2322002",
        'password': "60",
    }
    # wrong url
    test12 = {
        'username': "a2322002",
        'password': "6018As00_",
        'nickname': "gw",
        'url': "httadfp://192.23.4s2",
        'mobile': "+86.123482974401",
        'magic_number': 12
    }

    def test_register_params_check(self):
        # self.assertEqual(register_params_check(None), ("ok", True))
        self.assertEqual(register_params_check(self.test1), ("ok", True))
        self.assertEqual(register_params_check(self.test2), ("can not find username", False))
        self.assertEqual(register_params_check(self.test3), ("can not find password", False))
        self.assertEqual(register_params_check(self.test4), ("can not find nickname", False))
        self.assertEqual(register_params_check(self.test5), ("can not find url", False))
        self.assertEqual(register_params_check(self.test6), ("can not find mobile", False))
        self.assertEqual(register_params_check(self.test7), ("ok", True))
        self.assertEqual(register_params_check(self.test8), ("wrong username", False))
        self.assertEqual(register_params_check(self.test9), ("wrong username", False))
        self.assertEqual(register_params_check(self.test10), ("wrong password", False))
        self.assertEqual(register_params_check(self.test11), ("wrong password", False))
        self.assertEqual(register_params_check(self.test12), ("wrong url", False))

if __name__ == '__main__':
    unittest.main()
