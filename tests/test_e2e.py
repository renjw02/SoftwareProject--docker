import logging
import sys
import time
import unittest

import kthread
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from app import create_app, db
from app.models.model import User
from app.utils.jwt import encrypt_password

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class SeleniumTestCase(unittest.TestCase):
    client: WebDriver

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # You need to change this to your actual binary path.
        # options.binary_location = "C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
        options.binary_location = r"C:\Users\rjw2002\AppData\Local\Google\Chrome\Application\chrome.exe"
        # You need to change this to your actual web driver path.
        # cls.client = webdriver.Chrome(
        #     'drivers/chromedriver.exe', chrome_options=options)
        cls.client = webdriver.Chrome(
            'D://drivers/chromedriver.exe', chrome_options=options)

        # create the application
        cls.app = create_app('test')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # create the database and populate with some fake data
        db.drop_all()
        db.create_all()
        me = User(username="test", password=encrypt_password(str("test")), nickname="test",
                  mobile="+86.123456789012", magic_number=0, url="https://baidu.com")
        db.session.add(me)
        db.session.commit()

        # start the Flask server in a thread
        cls.server_thread = kthread.KThread(target=cls.app.run,
                                            kwargs={'debug': False})
        cls.server_thread.start()

        # give the server a second to ensure it is up
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

        # remove application context
        cls.app_context.pop()
        cls.server_thread.kill()

        # destroy database
        db.session.remove()
        db.drop_all()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_web(self):
        """
        EXAMPLE: 使用测试用户进行登录
        """
        self.client.get('http://127.0.0.1:5000')
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/a").click()
        self.client.find_element_by_id('username').send_keys('test')
        self.client.find_element_by_id('password').send_keys('test')
        self.client.find_element_by_xpath(
            '//*[@id="root"]/div/div[3]/div/button').click()
        time.sleep(3)
        """
        TODO: 登录后发帖，发帖标题为：Hello World，发帖内容为：你好！
        """
        # //*[@id="root"]/div/div[3]/div/div[1]/div/a
        # self.client.get('http://127.0.0.1:5000/submit-post')
        self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[1]/div/a').click()
        # self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div/input').send_keys("Hello World")
        # self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[2]/section[1]/textarea').send_keys("你好！")
        self.client.find_element_by_tag_name('input').send_keys("Hello World")
        self.client.find_element_by_name('textarea').send_keys('你好！')
        self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/button').click()
        # self.client.find_element_by_tag_name('button').click()
        time.sleep(3)
        

        """
        TODO: 更新帖子标题为：Hello World！，帖子内容为：你好。
        """
        # self.client.get('http://127.0.0.1:5000/edit-post/1')
        self.client.find_element_by_xpath('//*[@id="post-main"]/div[2]/span[2]/span/a[1]').click()
        self.client.find_element_by_tag_name('input').send_keys(Keys.CONTROL, 'a')
        self.client.find_element_by_tag_name('input').send_keys(Keys.DELETE)
        self.client.find_element_by_tag_name('textarea').send_keys(Keys.CONTROL, 'a')
        self.client.find_element_by_tag_name('textarea').send_keys(Keys.DELETE)
        self.client.find_element_by_tag_name('input').send_keys("Hello World!")
        self.client.find_element_by_tag_name('textarea').send_keys('你好。')
        self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/button').click()
        time.sleep(3)

        """
        TODO: 回复刚才的帖子，回复内容为：你好！
        """
        # self.client.get('http://127.0.0.1:5000/reply/1')
        self.client.find_element_by_xpath('//*[@id="post-main"]/div[2]/span[2]/span/a[2]').click() 
        self.client.find_element_by_tag_name('textarea').send_keys('你好!')
        # self.client.find_element_by_tag_name('button').click()
        self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/button').click()
        time.sleep(3)

        """
        TODO: 退出登录
        """
        # self.client.get('http://127.0.0.1:5000/user')
        self.client.find_element_by_xpath('//*[@id="root"]/div/header/div/span/a').click()
        self.client.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[6]/button').click()
        # self.client.find_element_by_tag_name('button').click()


if __name__ == '__main__':
    unittest.main()
