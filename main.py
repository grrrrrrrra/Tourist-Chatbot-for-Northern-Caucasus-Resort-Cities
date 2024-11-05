# from time import sleep
from math import ceil
import random
import os
from uuid import uuid4
import speech_recognition as sr
from telebot import types, TeleBot
from transliterate import translit
from pypinyin import lazy_pinyin

bot = TeleBot(open("TOKEN.txt", "r", encoding="utf-8").read())
add = "additions"
Start_path = "DB"
On_page = 5  # on page
Max_page = 5  # max page
All_city = []
All_attractions = []
Chinese_names = {}


# bot.send_message(1413931218,"Bot is working")


def updDB():  # обновляет данные: тексты, кртинки
    All_city.clear()
    All_attractions.clear()
    Chinese_names.clear()
    for Language1 in (os.listdir(Start_path)):
        if Language1 == "中文":
            Chinese_names[" ".join(lazy_pinyin(Language1))] = Language1
        for City1 in (os.listdir(Start_path + "/" + Language1)):
            if Language1 == "中文":
                Chinese_names[" ".join(lazy_pinyin(City1))] = City1
            All_city.append(City1.lower())
            for Atrracations1 in (os.listdir(Start_path + "/" + Language1 + "/" + City1)):
                All_attractions.append(Atrracations1.lower())
                if Language1 == "中文":
                    Chinese_names[(" ".join(lazy_pinyin(Atrracations1))).lower()] = Atrracations1.lower()
    print(All_city, All_attractions, Chinese_names, sep="\n")


updDB()


def updpopular():  # обновляет 10 наиболее популярных запросов
    global popular
    popular = {}
    for m in (os.listdir("Messege")):
        mess = open("Messege/" + m, "r", encoding="utf-8").read().replace("/", "").replace("_", " ").lower()
        mess = translit(mess, "ru", reversed=True)
        if mess in os.listdir(Start_path) or mess in All_city:
            continue
        elif mess in popular.keys():
            popular[mess] += 1
        elif mess.lower() in All_attractions or translit(mess, "ru",
                                                         reversed=True).lower() in All_attractions or translit(mess,
                                                                                                               "ru") in All_attractions:
            popular[mess] = 1
    popular = sorted(popular.items(), key=lambda item: item[1], reverse=True)
    print(popular[:10])


updpopular()


@bot.message_handler(commands=['sendyorescode'])  # отправляет текст кода админу по частям
def send_code(message):
    print(message.chat.id, ">", message.text)
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        c = ((str(open(str("TBot.py"), "r", encoding="utf-8").read()))[:874]) \
            + (str(open("TBot.py", "r", encoding="utf-8").read()))[1114:]
        parts = 5  #
        for li in range(0, parts):
            bot.send_message(message.chat.id, c[int((len(c) / parts) * li):int((len(c) / parts) * (li + 1))])
        t = str(message.from_user.id) + " " + str(message.from_user.first_name) + " " + str(
            message.from_user.last_name) + " " + str(message.from_user.username)
        m = "Следующий человечек чекнул код бота: " + t.replace("NONE", "...")
        bot.send_message(1413931218, m)


@bot.message_handler(commands=['popular'])  # отправляет 10 наиболее популянрных
def popular(message):
    active_language = open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[0]
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        updpopular()
    if active_language == "Русский":
        text = "Часто ищут:\n"
    elif active_language == "Русский":
        text = "Часто ищут:\n"
    else:
        text = "Often looking for:\n"
    for po in range(0, 10):
        text += "\n" + str(po + 1) + ") " + translit(("".join(popular[po][0])).replace("_", " ").capitalize(),
                                                     "ru") + "\n       /" + (
                    "R" if active_language == "Русский" else "C") + (
                    "".join(popular[po][0])).replace(" ", "_")
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['message'])  # для отправки сообщений от админа пользователю через бота
def admin_message(message):
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        message.text = message.text.replace("/mesage ", "")
        bot.send_message(message.text.split(" ")[0],
                         str(message.chat.id) + " > " + message.text.replace(message.text.split[0], ""))
        print(message.chat.id, ">", message.text)


@bot.message_handler(commands=['users'])  # отсылает админу полное имя всех пользователей бота
def Userlist(message):
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        print(message.chat.id, ">", message.text)
        for chatid in os.listdir("Users"):
            user = (open("Users/" + chatid, "r", encoding="utf-8").read().splitlines()[:5])
            bot.send_message(message.chat.id, ("\n".join(user)).replace("'", "").replace("{", "").replace(",", ""))


@bot.message_handler(commands=['help'])  # команда help
def Help(message):
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        bot.send_message(message.chat.id, "Для админов работают следующие команды:"
                                          "\n/users - для вывода списка пользователей."
                                          "\n/message - для отправки сообщений в формате: "
                                          "\n'/mesage chatid(первая строка /users) текст сообщения'"
                                          "\n/sendyorescode - присылает актуальный код бота"
                         )
    if open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[0] == "Русский":
        bot.send_message(message.chat.id, "В данный момент работают следующие команды:"
                                          "\n/help - для вывода данного меню "
                                          "\n/popular - выводит 10 самых популярных достопримечательностей "
                         )
    if open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[0] == "中文":
        bot.send_message(message.chat.id, "The next commands works:"
                                          "\n/help - for displaying this menu "
                                          "\n/popular - displays the 10 most popular attractions"
                         )
    else:
        bot.send_message(message.chat.id, "The next commands works:"
                                          "\n/help - for displaying this menu "
                                          "\n/popular - displays the 10 most popular attractions"
                         )
    print(message.chat.id, " попросил помощи")


# добавляет кнопки перелистывания вариантов сообщения в боте
def add_button(p, markup):
    button = [types.InlineKeyboardButton(text="1", callback_data="1")]
    for o in range(len(p) // On_page):
        button.append(types.InlineKeyboardButton(text=str(o + 2), callback_data=str(o + 2)))
    J = ceil(len(p) / On_page)
    if J == 2:
        markup.add(button[0], button[1])
    elif J == 3:
        markup.add(button[0], button[1], button[2])
    elif J == 4:
        markup.add(button[0], button[1], button[2], button[3])
    elif J == 5:
        markup.add(button[0], button[1], button[2], button[3], button[4])
    elif J == 6:
        markup.add(button[0], button[1], button[2], button[3], button[4], button[5])
    elif J == 7:
        markup.add(button[0], button[1], button[2], button[3], button[4], button[5], button[6])
    elif J == 8:
        markup.add(button[0], button[1], button[2], button[3], button[4], button[5], button[6], button[7])


#
def findpath(message):
    oldpath = open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read()
    open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write("")
    for variant_lenguage in os.listdir(Start_path):
        if message.text == variant_lenguage.lower():
            continue
        for variant_city in (os.listdir(Start_path + "/" + variant_lenguage)):
            if message.text == variant_city.lower():
                open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write(variant_lenguage + "/")
                continue
            for variant_attraction in (os.listdir(Start_path + "/" + variant_lenguage + "/" + variant_city)):
                if message.text == variant_attraction.replace(".txt", "").lower():
                    open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write(
                        variant_lenguage + "/" + variant_city + "/")
                    continue
    if open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read() == "":
        open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write(oldpath)


@bot.message_handler(commands=['start'])
def start(message, callback=None, page=0):
    page_ = (1 if page == 0 else page)
    if page == 0:
        open("Messege/" + str(message.chat.id) + "A" + str(message.id) + ".txt", "w", encoding="utf-8").write(
            message.text)
        open("Users/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write(
            str(message.from_user).replace(",", ",\n"))
    print(message.chat.id, ">", message.text)

    # привествие
    bot.send_message(message.chat.id,
                     "    Hello, dear friend! This is a tourist chatbot for the resort cities of the North Caucasus. "
                     "    The bot works in Russian and Chinese and will help reduce the time spent searching for up-to-date information about sights."
                     "\nIf you have any questions, please contact the administrator @Migel148 "
                     "\nBefore you start, select the language!", reply_markup=(types.ReplyKeyboardRemove(True)))
    if message.id < 5:
        Help(message)
    varriants = os.listdir(Start_path)
    Text = "Page: " + str(page_) + "\nChoose the lenguage:\n"

    if len(varriants) <= On_page:
        for si in range(len(varriants)):
            if varriants[si] == "Русский":
                Text += "\n" + str(si + 1) + ") " + varriants[si] + "\n" + "    " + "/R" + translit(varriants[si], "ru",
                                                                                                    reversed=True)
            elif varriants[si] == "中文":
                Text += "\n" + str(si + 1) + ") " + varriants[si] + "\n" + "     " + "/" + "C" + (
                    "_".join(lazy_pinyin(varriants[si])))
        bot.send_message(message.chat.id, Text)

    elif len(varriants) // On_page <= Max_page:
        inlineMarkup = types.InlineKeyboardMarkup(row_width=int((len(varriants)) // On_page) + 1)
        add_button(varriants, inlineMarkup)
        for si in range((page_ - 1) * On_page,
                        (len(varriants) % On_page + ((page_ - 1) * On_page) if (
                                page_ == (len(varriants) // On_page) + 1) else (page_ * On_page))):
            Text += "\n" + str(si + 1) + ") " + varriants[si].replace(".txt",
                                                                      "") + "\n" + "    " + "/" + translit(
                varriants[si].replace(".txt", ""), "ru", reversed=True)
        if page == 0:
            bot.send_message(message.chat.id, Text, reply_markup=inlineMarkup)
        else:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=callback.message.text, reply_markup=callback.message.reply_markup)
    else:
        print("Чёт многовато языков!")

    open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write("")
    if str(message.chat.id) in open("Adminlist.txt", "r").read().splitlines():
        updDB()


def city(message, callback=None, page=0):  #
    page_ = (1 if page == 0 else page)
    if message.text == "Русский":
        Text = "Страница: " + str(page_) + "\nВыберите город для путешествия:\n"
    elif message.text == "中文":
        Text = "页面: " + str(page_) + "\n选择旅行的城市:\n"
    else:
        Text = "Page" + str(page_) + "\nChoose the city:\n"
    Cities = os.listdir(Start_path + "/" + message.text)

    if len(Cities) // On_page <= Max_page:
        inlineMarkup = types.InlineKeyboardMarkup(row_width=int((len(Cities)) // On_page) + 1)
        add_button(Cities, inlineMarkup)
        for ci in range((page_ - 1) * On_page,
                        (len(Cities) % On_page + ((page_ - 1) * On_page) if (
                                page_ == (len(Cities) // On_page) + 1) else (page_ * On_page))):
            if message.text == "Русский":
                Text += "\n" + str(ci + 1) + ") " + Cities[ci] + "\n" + "     " + "/" + "R" + translit(
                    Cities[ci].replace(" ", "_"), "ru", reversed=True)
            elif message.text == "中文":
                Text += "\n" + str(ci + 1) + ") " + Cities[ci] + "\n" + "     " + "/" + "C" + ("_".join(
                    lazy_pinyin(Cities[ci])).replace(" ", "_"))
        else:
            inlineMarkup = None
        if page == 0:
            bot.send_message(message.chat.id, Text, reply_markup=inlineMarkup)
        else:
            if Text.replace("\n", "") != callback.message.json["text"].replace("\n", ""):
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id + 1, text=Text,
                                      reply_markup=callback.message.reply_markup)
    else:
        print("Чёт многовато городов!")

    m1 = bot.send_message(message.chat.id, "1", reply_markup=types.ReplyKeyboardRemove(True))
    bot.delete_message(message.chat.id, m1.id)


def attractions(message, callback=None, page=0):  #
    page_ = (1 if page == 0 else page)
    language = open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[0]

    # Вступительный текст по городам
    if page_ == 1 and os.path.isfile(
            add + "/" + open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read()
            + "/" + message.text + ".txt"):
        Text = "\n" + (open(add + "/" + open("UaP" + "/" + str(message.chat.id) + ".txt", "r",
                                             encoding="utf-8").read() + "/" + message.text + ".txt", "r",
                            encoding="utf-8").read()) + "\n\n"
    else:
        Text = message.text.capitalize() + ". "
    if language == "Русский":
        Text += "Страница: " + str(page_) + "\nВыберите достопримечательность:\n"
    elif language == "中文":
        Text = "页面: " + str(page_) + "\n选择一个旅游景点:\n"
    else:
        Text += "Page: " + str(page_) + "\nChoose the place:\n"
    Attractions = os.listdir(
        Start_path + "/" + open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[
            0] + "/" + message.text)
    if len(Attractions) // On_page <= Max_page:
        for di in range((page_ - 1) * On_page,
                        (len(Attractions) % On_page + ((page_ - 1) * On_page) if (
                                page_ == (len(Attractions) // On_page) + 1) else (
                                page_ * On_page))):
            if language == "Русский":
                Text += "\n" + str(di + 1) + ") " + Attractions[di].replace(".txt",
                                                                            "") + "\n" + "     " + "/" + "R" + translit(
                    Attractions[di].replace(".txt", "").replace(" ", "_"), "ru", reversed=True)
            elif language == "中文":
                Text += "\n" + str(di + 1) + ") " + Attractions[di].replace(".txt",
                                                                            "") + "\n" + "     " + "/" + "C" + "_".join(
                    lazy_pinyin(
                        Attractions[di].replace(".txt", "")))
        if len(Attractions) > On_page:
            inlineMarkup = types.InlineKeyboardMarkup(row_width=int((len(Attractions)) // On_page) + 1)
            add_button(Attractions, inlineMarkup)
        else:
            inlineMarkup = None
        if page == 0:
            bot.send_message(message.chat.id, Text, reply_markup=inlineMarkup)
        else:
            if Text.replace("\n", "") != callback.message.json["text"].replace("\n", ""):
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id + 1, text=Text,
                                      reply_markup=callback.message.reply_markup)
                # bot.send_message(callback.message.chat.id, 111)
    else:
        print("Чёт многовато достопримечательностей!")


@bot.message_handler(content_types=['text'])  # при любых текстовых сообщениях, которые не распознались ранее
def mesegereply(message, callback=None, page=0):  #
    message.text = message.text.replace("_", " ")
    if message.text[0] == "/":  #
        if message.text[1] == "R":
            message.text = translit(message.text[2:], "ru")
        elif message.text[1] == "C":
            message.text = message.text[2:]
            message.text = Chinese_names[message.text.lower()]
    # sleep(1)
    # создание "логов"
    if page == 0 and message.text != "Назад" and message.text != "Come back" and \
            (message.text.lower() in All_attractions or message.text.lower() in All_city or not (
                    message.text in os.listdir(Start_path))):
        open("Messege/" + str(message.chat.id) + "A" + str(message.id) + ".txt", "w", encoding="utf-8").write(
            message.text)
        message.text = message.text.lower()
        findpath(message)
        print(("Супер-админ" if message.chat.id == 1413931218 else message.chat.id), (
            open("Users/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().splitlines()[3][12:].replace(
                ",", "-", 1)) + "->", message.text,
              open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read())
    elif message.text in os.listdir(Start_path):
        print(message.chat.id, ">", message.text, "(" + translit(message.text, "ru") + ")",
              open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read())
    elif callback is not None:
        print(message.chat.id, ">", "Меняет страницу")
    elif callback.data == "Come back" or message.text == "Назад" or message.text == "Come back" or message.text == "回去":
        pass
    else:
        print("Что-то нетипичное происходит, " + str(message.chat.id) + " ищет " + message.text)

    path = open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[:-1]
    actualdirectory = str((("/" + path[0]) if len(path) > 0 else "") + (("/" + path[1]) if len(
        path) > 1 else "") + "/" + message.text)

    if message.text in (os.listdir(Start_path)):
        city(message, callback, page)
    elif message.text.lower() in All_city:
        attractions(message, callback, page)
    elif message.text.lower() in All_attractions or message.text.lower() + ".txt" in All_attractions \
            or message.text.lower() + ".jpg" in All_attractions:

        files_in_directory = os.listdir(Start_path + actualdirectory)

        inlineMarkup = types.InlineKeyboardMarkup(row_width=3)
        print(files_in_directory)
        if "coordinates.txt" in files_in_directory:
            button = types.InlineKeyboardButton(text="1", callback_data="1")
            inlineMarkup.add(button)

        if os.path.exists(Start_path + actualdirectory + "/" + message.text + ".png"):
            print(len(Start_path + "/" + path[0] + "/" + path[1] + "/" + message.text + "/" + message.text + ".png"),
                  len(actualdirectory))
            inlineMarkup.add(types.InlineKeyboardButton(text=str(f"Картинка"), callback_data=message.text + ".png"))
        inlineMarkup.add(types.InlineKeyboardButton(text=open(f"{add}/{path[0]}/Cb.txt","r",encoding="utf-8").read(), callback_data="Come back"))
        if os.path.exists(
                Start_path + "/" + path[0] + "/" + path[1] + "/" + message.text + "/" + message.text + ".txt"):
            bot.send_message(message.chat.id, open(
                Start_path + "/" + path[0] + "/" + path[1] + "/" + message.text + "/" + message.text + ".txt",
                "r", encoding="utf-8").read(), reply_markup=inlineMarkup)
    #

    elif callback.data == "Come back" or message.text == "Назад" or message.text == "Come back" or message.text == "回去":  #
        b1 = ""
        for bi in range(len(path) - 2):
            b1 += path[bi] + "/"
            open("UaP" + "/" + str(message.chat.id) + ".txt", "w", encoding="utf-8").write(b1)
            bot.delete_message(message.chat.id, message.id)

        try:
            message.text = path[-1]
            mesegereply(message)
        except IndexError:
            print(message.chat.id, "> многовато жал на кнопку")
            if path != []:
                bot.send_message(message.chat.id,open(f"{add}/{path[0]}/C&W.txt","r",encoding="utf-8").read())
            else:
                bot.send_message(message.chat.id, "Click the button once and wait for it to load")
    elif message.text == "start":  #
        start(message, callback, page)
    #
    else:
        if len(message.text) > 0:
            varilist = ""
            for Atraction in All_attractions:
                if message.text in Atraction:
                    if Atraction in Chinese_names.values():
                        varilist += "\n" + " " + Atraction.title() + "\n" + "    " + "/C" + " ".join(
                            lazy_pinyin(Atraction)).replace(" ", "_") + "\n"
                    else:
                        varilist += "\n" + " " + Atraction.title() + "\n" + "    " + "/R" + translit(Atraction, "ru",
                                                                                                     reversed=True).replace(
                            " ", "_") + "\n"
            if varilist == "":  #
                bot.send_message(message.chat.id, random.choice(
                    (open(add + "/" + (path[0] if path != [] else "English") + "/" + "Notfound.txt", "r",
                          encoding="utf-8").read().splitlines())))
            else:
                bot.send_message(message.chat.id, random.choice(
                    open(add + "/" + (path[0] if path != [] else "English") + "/Variant.txt", "r",
                         encoding="utf-8").read().splitlines()) + varilist)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    message = callback.message
    message.id = (callback.message.id - 1)
    message.text = open("Messege/" + str(callback.message.chat.id) + "A" + str(callback.message.id) + ".txt", "r",
                        encoding="utf-8").read()
    if callback.data.isdigit():
        mesegereply(message, callback, int(callback.data))
    elif callback.data.split(".")[0] in All_attractions and callback.data.split(".")[-1] == "png":
        findpath(message)
        bot.send_photo(message.chat.id, open(
            str(Start_path + "/" + open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read() +
                callback.data.split(".")[0] + "/" + callback.data), "rb"))
    else:
        mesegereply(message, callback)


def recognise(filename, lenguage):  #
    with sr.AudioFile(filename) as source:
        if lenguage == "Русский":
            language = 'ru_RU'
        elif lenguage == "中文":
            language = 'ru_RU'
        r = sr.Recognizer()
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            return "..."


@bot.message_handler(content_types=['voice'])
def voice_processing(message):  #
    if message.voice.duration < 20:
        filename = str(uuid4())
        file_name_full = "voice/" + filename + ".ogg"
        file_name_full_converted = "ready/" + filename + ".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i " + file_name_full + "  " + file_name_full_converted)
        lenguage = open("UaP" + "/" + str(message.chat.id) + ".txt", "r", encoding="utf-8").read().split("/")[0]
        text = recognise(file_name_full_converted, lenguage)
        if len(text.split(" ")) > 1:
            for messageword in text.split(" "):
                if All_attractions.count(messageword.lower()) > 0:
                    message.text = messageword
                    break
        else:
            message.text = text
        if message.text == "...":
            bot.send_message(message.chat.id, random.choice((open(
                add + "/" + (lenguage[0] if lenguage != [] else "English") + "/" + "Notfound.txt", "r",
                encoding="utf-8").read().splitlines())))
        else:
            mesegereply(message)
        os.remove(file_name_full)
        os.remove(file_name_full_converted)


if __name__ == "__main__":
    bot.infinity_polling()
