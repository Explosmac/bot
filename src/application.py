import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.utils import Utils

def main():
    driver = Utils.load_page()
    username = 'explosm'
    password = 'qweqweqwe'
    Utils.login(driver, username, password)
    time.sleep(3)

    while True:
        Utils.start_play(driver)
        time.sleep(10)

    driver.close()

main()
