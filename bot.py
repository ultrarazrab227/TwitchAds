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

bot = telebot.TeleBot("6253091837:AAHtDY2BN-bnbyImKlJeiWEOwVpPq81OPQw")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id in config["users"]:
        bot.send_message(message.chat.id,
                         f"Добрый день, {message.from_user.first_name}. \n"
                         f"Вам доступен функционал бота. Для вывода списка команд напишите /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    if message.from_user.id in config["users"]:
        bot.send_message(message.chat.id, "Список команд:\n\n"
                                          "/thread [число потоков] - изменить число потоков\n"
                                          "/link [ссылка] - изменить ссылку на стрим")


file = __file__


@bot.message_handler(commands=['thread'])
def send_welcome(message):
    if message.from_user.id in config["users"]:
        #        try:
        ThreadsNum = extract_arg(message.text)
        if ThreadsNum.isdigit():
            config["ThreadsNum"] = int(ThreadsNum)
            update()
            print(file)
            subprocess.call([sys.executable, os.path.realpath(file)] + sys.argv[1:])
        else:
            bot.send_message(message.chat.id, "Вы ввели некоректное число потоков")


#        except:
#            bot.send_message(message.chat.id, "Произошла ошибка, попробуйте позже")


@bot.message_handler(commands=['link'])
def send_welcome(message):
    if message.from_user.id in config["users"]:
        link = extract_arg(message.text)
        if link[:22] == "https://www.twitch.tv/":
            config["link"] = link
            update()
            subprocess.call([sys.executable, os.path.realpath(file)] + sys.argv[1:])


bot.infinity_polling()
