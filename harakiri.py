import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
from time import sleep
from random import randint
import telebot

bot = telebot.TeleBot("6024479445:AAFA9azljzZtQpuuRQf7T6pU2F-81KoG6ps")

options = Options()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


def open_google():
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.twitch.tv/papaplatte')
    sleep(randint(15, 120))
    driver.quit()
    open_google()


if __name__ == '__main__':
    for i in range(1):
        t = threading.Thread(target=open_google)
        t.start()
