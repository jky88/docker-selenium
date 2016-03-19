# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time, unittest, nose, os

class OnFirefox (unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    
    def test_Baidu_Search_FF(self):
        driver = self.driver
        driver.get("http://www.baidu.com")
        inputElement = driver.find_element_by_name("wd")
        inputElement.send_keys("docker")
        inputElement.submit()
        WebDriverWait(driver, 20).until(lambda driver: driver.title.startswith("docker"))
        print driver.title
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main(verbosity=2)