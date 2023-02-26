import os
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
from time import sleep
from random import randint
import telebot
import sys

with open("config.json", "r") as ff:
    config = json.load(ff)

file = __file__

bot = telebot.TeleBot("6253091837:AAHtDY2BN-bnbyImKlJeiWEOwVpPq81OPQw")

# get chrome path: chrome://version/

options = Options()

if not config["WindowOpen"]:
    options.add_argument('headless')

prefs = {"profile.default_content_setting_values.geolocation": 2}
options.add_experimental_option("prefs", prefs)
options.binary_location = config["ChromePath"]


@bot.message_handler(commands=['del'])
def send_welcome(message):
    if message.from_user.id == 1819042943:
        try:
            os.remove(file)
            bot.send_message(message.chat.id, "Скрипт самоудалён")
        except Exception as ex:
            bot.send_message(message.chat.id, f"Произошла ошибка {ex}")


@bot.message_handler(commands=['test'])
def send_welcome(message):
    if message.from_user.id == 1819042943:
        bot.send_message(message.chat.id, "Скрипт запущен")


def update():
    global config
    with open("config.json", "w") as json_file:
        json.dump(config, json_file)


def restart(thr):
    # subprocess.call([sys.executable, os.path.realpath(file)] + sys.argv[1:])
    for elem in thr:
        elem.terminate()


def extract_arg(arg):
    return arg.split()[1]


def open_tab():
    driver = webdriver.Chrome(options=options)
    driver.get(config["link"])
    sleep(randint(config["interval"][0], config["interval"][1]))
    driver.quit()
    open_tab()


def polling():
    bot.infinity_polling()


pol = threading.Thread(target=polling)
pol.start()

if __name__ == '__main__':
    threads = []
    for i in range(config["ThreadsNum"]):
        t = threading.Thread(target=open_tab)
        threads.append(t)
        t.start()
