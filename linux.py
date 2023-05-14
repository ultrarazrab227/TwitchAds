import os
from selenium import webdriver

os.environ['PATH'] += "/media/alexv/DATA/python projects/TwitchAds/LinuxWebdriver"
driver = webdriver.Chrome()
driver.get("google.com")
