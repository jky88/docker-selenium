# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time, unittest, nose, os

class OnChrome (unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
    
    def test_Yunqi_Search_Chrome(self):
        driver = self.driver
        driver.get("https://yq.aliyun.com/")
        inputElement = driver.find_element_by_name("q")
        inputElement.send_keys("docker")
        inputElement.submit()
        WebDriverWait(driver, 20).until(lambda driver: driver.title == u"搜索-云栖社区")
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main(verbosity=2)