from googletrans import Translator
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import time
import os



bot_token = "6387632922:AAFnuvIbuBMhyFNtA9ab9DyPM1ohRP8cXEM"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: message.text.strip().lower() in ['ترجمة', 'ترجمه'])
def translate(message):
    translator = Translator()
    text = (" ذهبت ")
    target_language = ("en")
    translation = translator.translate(text, dest=target_language)
    bot.reply_to(message, f"الترجمة: {translation.text}")


       

if __name__ == "__main__":
    while True:
        try:
            print("working...")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(5) 
