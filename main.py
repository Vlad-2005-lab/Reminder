# types.ReplyKeyboardRemove() - удаление клавиатуры
from data.users import User
from data.tasks import Task
from data import db_session
from datetime import timezone
import time
import datetime
import telebot  # скачать надо pip install pytelegrambotapi
from telebot import types
import pytz
from emoji import emojize
import threading
import schedule
import yadisk

yandex_disk = yadisk.YaDisk(token="AQAAAAA1zbBwAAdMqNcOyvthqEaaltCqQTkwV8s")
try:
    yandex_disk.download("my.sqlite", "bd/my.sqlite")
except Exception:
    yandex_disk.upload("bd/my.sqlite", "my.sqlite")
try:
    db_session.global_init("bd/my.sqlite")
except Exception:
    db_session.global_init("C:/Users/Айдар/PycharmProjects/rfu/bd/my.sqlite")
print("\033[35mдб подключилась")
bot = telebot.TeleBot(open('data/token.txt').read().split()[0])  # строка
SMILE = ['↩', "🏠", "❌"]
count = -1
history = True
timezones = ["Europe/Kaliningrad", "Europe/Moscow", "Europe/Samara", "Asia/Yekaterinburg", "Asia/Omsk",
             "Asia/Krasnoyarsk",
             "Asia/Irkutsk", "Asia/Chita", "Asia/Vladivostok", "Asia/Magadan", "Asia/Anadyr", "Africa/Abidjan"]


def log(message=None, where='ne napisal', full=False, comments="None"):
    """[
    :param message: class; ответ из тг(message_handler)
    :param where: str; место(имя функции) где вызывается эта функция
    :param full: True/False
    :param comments: str; хз, любой ваш коментарий
    :return: в консоль пишет лог
    """
    global count, history
    count += 1
    if history:
        history = False
        print("""\033[33mWriting history started:\033[30m""")
    elif full:
        try:
            print(f"""\033[33m{"-" * 100}
time: \033[36m{tconv(message.date)}\033[33m
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: {message.text}
message: \033[35m{message}\033[33m
comments: \033[31m{comments}\033[33m""")
        except Exception as er:
            print(f"""\033[31m{"-" * 100}\n!ошибка, лог №{count}\n message: {message}
where: {where}
full: {full}\033
comments: {comments}
error: {er}[0m""")
    else:
        try:
            print(f"""\033[33m{"-" * 100}
time: \033[36m{tconv(message.date)}\033[33m
log №{count}
from: {where}
full: {full}
id: \033[36m{message.from_user.id}\033[33m
username: \033[36m{message.from_user.username}\033[33m
first_name(имя): \033[36m{message.from_user.first_name}\033[33m
last_name(фамилия): \033[36m{message.from_user.last_name}\033[33m
text: \033[35m{message.text}\033[33m
comment: {comments}\033[0m""")
        except Exception as er:
            print(f"""\033[31m!ошибка! Лог №{count}\n message: {message}
time: \033[36m{datetime.datetime.now()}\033[33m
where: {where}
full: {full}
comments: {comments}
error: {er}\033[0m""")


def get_delta(a):
    return a.seconds + a.days * 24 * 60 * 60


def tconv(x):
    """
    :param x: int; хз что передаётся, вроде секунды
    :return: str; нормально выглядещую дату и время
    """
    return time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


def keyboard_creator(list_of_names, one_time=True):
    """
    :param list_of_names: list; это список с именами кнопок(['1', '2'] будет каждая кнопка в ряд)
    [['1', '2'], '3'] первые 2 кнопки будут на 1 линии, а 3 снизу)
    :param one_time: bool; скрыть клаву после нажатия или нет
    :return: готовый класс клавиатуры в низу экрана
    """
    returned_k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    for i in list_of_names:
        if isinstance(i, list):
            string = ""
            for o in range(len(i) - 1):
                string += f"'{i[o]}', "
            string += f"'{i[-1]}'"
            exec(f"""returned_k.row({string})""")
            continue
        exec(f"""returned_k.row('{i}')""")
    return returned_k


def buttons_creator(dict_of_names, how_many_rows=8):
    """
    :param dict_of_names: dict; это словарь, первые ключи могут быть любыми, они разделяют кнопки на ряды, а значениями этих ключей
           являются другие словари. Первый их аргумент это текст кнопки, а 2 это callback_data(то что будет передаваться в
           коллбек). Например: {
                                   '1': {
                                       'текст первой кнопки': 'нажали на кнопку 1',
                                       'текст второй кнопки': 'нажали на кнопку 2'
                                       },
                                   '2': {
                                       'текст третьей кнопки': 'нажали на кнопку 3'
                                       }
                               }
    :param how_many_rows: int; это максимальное количество кнопок в ряду
    :return: готовый класс кнопок под сообщением
    """
    returned_k = types.InlineKeyboardMarkup(row_width=how_many_rows)
    for i in dict_of_names.keys():
        if type(dict_of_names[i]) is dict:
            count = 0
            for o in dict_of_names[i].keys():
                count += 1
                exec(
                    f"""button{count} = types.InlineKeyboardButton(text='{o}', callback_data='{dict_of_names[i][o]}')""")
            s = []
            for p in range(1, count + 1):
                s.append(f"button{p}")
            exec(f"""returned_k.add({', '.join(s)})""")
        else:
            exec(f"""button = types.InlineKeyboardButton(text='{i}', callback_data='{dict_of_names[i]}')""")
            exec(f"""returned_k.add(button)""")
    return returned_k


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    keyboard = keyboard_creator(["МСК - 1, (UTC +2)",
                                 "МСК, (UTC +3)",
                                 "МСК + 1, (UTC +4)",
                                 "МСК + 2, (UTC +5)",
                                 "МСК + 3, (UTC +6)",
                                 "МСК + 4, (UTC +7)",
                                 "МСК + 5, (UTC +8)",
                                 "МСК + 6, (UTC +9)",
                                 "МСК + 7, (UTC +10)",
                                 "МСК + 8, (UTC +11)",
                                 "МСК + 9, (UTC +12)"])
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    try:
        keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                     ["Изменить часовой пояс",
                                      f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                     "Удалить аккаунт"])
        bot.send_message(message.from_user.id,
                         "Вы в главном меню",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, main_menu)
    except Exception:
        bot.send_message(message.from_user.id,
                         f"Здраствуйте, для того чтобы сделать напоминание, выберите свой часовой пояс",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, select_utc)


def select_utc(message):
    keyboard = keyboard_creator(["МСК - 1, (UTC +2)",
                                 "МСК, (UTC +3)",
                                 "МСК + 1, (UTC +4)",
                                 "МСК + 2, (UTC +5)",
                                 "МСК + 3, (UTC +6)",
                                 "МСК + 4, (UTC +7)",
                                 "МСК + 5, (UTC +8)",
                                 "МСК + 6, (UTC +9)",
                                 "МСК + 7, (UTC +10)",
                                 "МСК + 8, (UTC +11)",
                                 "МСК + 9, (UTC +12)"])
    session = db_session.create_session()
    user = User()
    user.tg_id = message.from_user.id
    if message.text == "МСК - 1, (UTC +2)":
        user.time_zone = 2
    elif message.text == "МСК, (UTC +3)":
        user.time_zone = 3
    elif message.text == "МСК + 1, (UTC +4)":
        user.time_zone = 4
    elif message.text == "МСК + 2, (UTC +5)":
        user.time_zone = 5
    elif message.text == "МСК + 3, (UTC +6)":
        user.time_zone = 6
    elif message.text == "МСК + 4, (UTC +7)":
        user.time_zone = 7
    elif message.text == "МСК + 5, (UTC +8)":
        user.time_zone = 8
    elif message.text == "МСК + 6, (UTC +9)":
        user.time_zone = 9
    elif message.text == "МСК + 7, (UTC +10)":
        user.time_zone = 10
    elif message.text == "МСК + 8, (UTC +11)":
        user.time_zone = 11
    elif message.text == "МСК + 9, (UTC +12)":
        user.time_zone = 12
    else:
        bot.send_message(message.from_user.id,
                         "Извините, но такого варианта нет, попробуйте ещё раз",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, select_utc)
    session.add(user)
    session.commit()
    keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                 ["Изменить часовой пояс",
                                  f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                 "Удалить аккаунт"])
    bot.send_message(message.from_user.id,
                     "Хорошо, теперь вы в главном меню",
                     reply_markup=keyboard)
    return bot.register_next_step_handler(message, main_menu)


def change_utc(message):
    keyboard = keyboard_creator(["МСК - 1, (UTC +2)",
                                 "МСК, (UTC +3)",
                                 "МСК + 1, (UTC +4)",
                                 "МСК + 2, (UTC +5)",
                                 "МСК + 3, (UTC +6)",
                                 "МСК + 4, (UTC +7)",
                                 "МСК + 5, (UTC +8)",
                                 "МСК + 6, (UTC +9)",
                                 "МСК + 7, (UTC +10)",
                                 "МСК + 8, (UTC +11)",
                                 "МСК + 9, (UTC +12)"])
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if message.text == "МСК - 1, (UTC +2)":
        user.time_zone = 2
    elif message.text == "МСК, (UTC +3)":
        user.time_zone = 3
    elif message.text == "МСК + 1, (UTC +4)":
        user.time_zone = 4
    elif message.text == "МСК + 2, (UTC +5)":
        user.time_zone = 5
    elif message.text == "МСК + 3, (UTC +6)":
        user.time_zone = 6
    elif message.text == "МСК + 4, (UTC +7)":
        user.time_zone = 7
    elif message.text == "МСК + 5, (UTC +8)":
        user.time_zone = 8
    elif message.text == "МСК + 6, (UTC +9)":
        user.time_zone = 9
    elif message.text == "МСК + 7, (UTC +10)":
        user.time_zone = 10
    elif message.text == "МСК + 8, (UTC +11)":
        user.time_zone = 11
    elif message.text == "МСК + 9, (UTC +12)":
        user.time_zone = 12
    else:
        bot.send_message(message.from_user.id,
                         "Извините, но такого варианта нет, попробуйте ещё раз",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, change_utc)
    session.commit()
    keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                 ["Изменить часовой пояс",
                                  f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                 "Удалить аккаунт"])
    bot.send_message(message.from_user.id,
                     f"Ваш пояс сменён на:\nМСК {f'+ {user.time_zone - 3}' if user.time_zone else ''}, " +
                     f"(UTC +{user.time_zone})",
                     reply_markup=keyboard)
    return bot.register_next_step_handler(message, main_menu)


def task_user(message):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    task = Task()
    task.tg_id = message.from_user.id
    task.name = message.text
    session.add(task)
    session.commit()
    user.list_of_tasks = ' '.join((user.list_of_tasks.split() + [str(task.id)]))
    session.commit()
    bot.send_message(message.from_user.id,
                     f"Введите дату в формате: часы:минуты день.месяц.год(20:20 15:09:2021)",
                     reply_markup=types.ReplyKeyboardRemove())
    return bot.register_next_step_handler(message, time_task)


def time_task(message):
    try:
        session = db_session.create_session()
        task = session.query(Task).filter(Task.tg_id == message.from_user.id).all()[-1]
        user = session.query(User).filter(User.tg_id == message.from_user.id).first()
        tak_nado = message.text.split()
        hours = list(map(int, tak_nado[0].split(":")))
        date = list(map(int, tak_nado[1].split(".")))
        utcmoment_naive = datetime.datetime.utcnow()
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        time_now = utcmoment.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
        print(message.date)
        print(tconv(message.date))
        # try:
        #     last_time = datetime.datetime.strptime(str(task.last_time), '%Y-%m-%d %H:%M:%S.%f%z')
        # except Exception:
        #     last_time = datetime.datetime.fromtimestamp(float(task.last_time), timezone.utc)
        if len(str(date[2])) == 4 and 0 <= hours[0] <= 23 and 0 <= hours[1] <= 59 and (
                1 <= date[0] <= 31 and date[1] in [1, 3, 5, 7, 8, 10, 12] or 1 <= date[0] <= 30 and date[1] in [4, 6, 9,
                                                                                                                11] or 1 <=
                date[0] <= 29 and date[1] == 2) and 1 <= date[1] <= 12:
            if get_delta((datetime.datetime(date[2], date[1], date[0], hours[0], hours[1],
                                            tzinfo=pytz.timezone(timezones[user.time_zone - 2])) - time_now)) > 0:
                huj = datetime.datetime(date[2], date[1], date[0], hours[0], hours[1])
                huj = datetime.datetime.fromtimestamp(huj.timestamp() - 3600 * user.time_zone)
                task.time = f"{huj.hour}:{huj.minute} {huj.day}.{huj.month}.{huj.year}"
                task.last_time = time_now
                session.commit()
                keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                             ["Изменить часовой пояс",
                                              f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                             "Удалить аккаунт"])
                bot.send_message(message.from_user.id,
                                 f"Вы создали себе напоминание:\nНазвание: {task.name}\nДата: {message.text}",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.from_user.id,
                                 f"Вы в главном меню",
                                 reply_markup=keyboard)
                return bot.register_next_step_handler(message, main_menu)
            else:
                print("+")
                bot.send_message(message.from_user.id,
                                 f"Вы ввели не правильно дату.\nВведите дату в формате: часы:минуты день.месяц.год",
                                 reply_markup=types.ReplyKeyboardRemove())
                return bot.register_next_step_handler(message, time_task)
        else:
            bot.send_message(message.from_user.id,
                             f"Вы ввели не правильно дату.\nВведите дату в формате: часы:минуты день.месяц.год",
                             reply_markup=types.ReplyKeyboardRemove())
            return bot.register_next_step_handler(message, time_task)
    except Exception as ex:
        bot.send_message(message.from_user.id,
                         f"Вы ввели не правильно дату.\nВведите дату в формате: часы:минуты день.месяц.год",
                         reply_markup=types.ReplyKeyboardRemove())
        return bot.register_next_step_handler(message, time_task)


def check(message):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    tasks = session.query(Task).filter(Task.tg_id == user.tg_id).all()
    if message.text == "Да":
        for task in tasks:
            session.delete(task)
            session.commit()
        session.delete(user)
        session.commit()
        bot.send_message(message.from_user.id,
                         f"Досвидания",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_sticker(message.from_user.id,
                         'CAACAgQAAxkBAAECtLxhD6Cf-LnR6qtYzfUc6xt6lOI93AACQQEAAqghIQavZsYbbe5LiyA')
        return bot.register_next_step_handler(message, get_text_messages)
    elif message.text == "Нет":
        keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                     ["Изменить часовой пояс",
                                      f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                     "Удалить аккаунт"])
        bot.send_message(message.from_user.id,
                         f"Удаление отменено, пользуйтесть нашим ботом дальше",
                         reply_markup=keyboard)
        bot.send_sticker(message.from_user.id,
                         'CAACAgQAAxkBAAECtL5hD6DtehBYXgfyvynX_b0MXkNbrQACMwEAAqghIQaDngab6f9thSAE')
        return bot.register_next_step_handler(message, main_menu)
    else:
        keyboard = keyboard_creator([["Да", "Нет"]])
        bot.send_message(message.from_user.id,
                         f"Такого варианта нет, попробуйте ещё раз",
                         reply_markup=keyboard)
        return bot.register_next_step_handler(message, check)


def main_menu(message):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                 ["Изменить часовой пояс",
                                  f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                 "Удалить аккаунт"])
    if message.text == "Создать напоминание":
        bot.send_message(message.from_user.id,
                         f"Введите название",
                         reply_markup=types.ReplyKeyboardRemove())
        return bot.register_next_step_handler(message, task_user)
    elif message.text == "Мои напоминания":
        keyboard = keyboard_creator([f"Вернуться в меню {emojize(SMILE[1], use_aliases=True)}"])
        bot.send_message(message.from_user.id, f"Начинаем поиск", reply_markup=keyboard)
        list_poiska = session.query(Task).filter(message.from_user.id == Task.tg_id).all()
        if len(list_poiska) != 0:
            key_dict = {'1': {}}
            if len(list_poiska) > 5:
                key_dict["1"]["<"] = "back"
            text = f"Страница 1 из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}\n\n"
            _list = []
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                try:
                    min_time = datetime.datetime.strptime(str(list_poiska[i].time), '%H:%M %d.%m.%Y')
                except Exception:
                    min_time = datetime.datetime.fromtimestamp(float(list_poiska[i].time), timezone.utc)
                min_time = min_time.replace(tzinfo=pytz.utc)
                min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
                string = f"{1 + i}. {list_poiska[i].name}\nДата: {str(min_time).split('+')[0]}"
                _list.append(string)
            text += "\n".join(_list)
            for i in range(1, len(_list) + 1):
                key_dict["1"][f"{i}"] = f"{i}"
            if len(list_poiska) > 5:
                key_dict["1"][">"] = "next"
            bot.send_message(message.from_user.id, text, reply_markup=buttons_creator(key_dict))
        else:
            keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                         ["Изменить часовой пояс",
                                          f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                         "Удалить аккаунт"])
            text = "У вас нет напоминаний"
            bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    elif message.text == "Изменить часовой пояс":
        keyboard = keyboard_creator(["МСК - 1, (UTC +2)",
                                     "МСК, (UTC +3)",
                                     "МСК + 1, (UTC +4)",
                                     "МСК + 2, (UTC +5)",
                                     "МСК + 3, (UTC +6)",
                                     "МСК + 4, (UTC +7)",
                                     "МСК + 5, (UTC +8)",
                                     "МСК + 6, (UTC +9)",
                                     "МСК + 7, (UTC +10)",
                                     "МСК + 8, (UTC +11)",
                                     "МСК + 9, (UTC +12)"])
        bot.send_message(message.from_user.id,
                         f"Ваш часовой пояс: МСК {f'+ {user.time_zone - 3}' if user.time_zone else ''}, " +
                         f"(UTC +{user.time_zone})\nВыберите новый",
                         reply_markup=keyboard)

        return bot.register_next_step_handler(message, change_utc)
    elif message.text == f"Уведомления ночью: {'on' if user.night_writing else 'off'}":
        user.night_writing = not user.night_writing
        session.commit()
        keyboard = keyboard_creator([["Создать напоминание", "Мои напоминания"],
                                     ["Изменить часовой пояс",
                                      f"Уведомления ночью: {'on' if user.night_writing else 'off'}"],
                                     "Удалить аккаунт"])
        bot.send_message(message.from_user.id,
                         f"Ночной режим изменён",
                         reply_markup=keyboard)
        bot.delete_message(message.chat.id, message.message_id)
    elif message.text == "Удалить аккаунт":
        keyboard = keyboard_creator([["Да", "Нет"]])
        bot.send_message(message.from_user.id, f"Вы уверены?", reply_markup=keyboard)
        bot.send_sticker(message.from_user.id,
                         'CAACAgQAAxkBAAECtMBhD6EKCcwy07V5AAE8TBh3vnIsWAcAAkIBAAKoISEGxyDfTJ2UTDcgBA')
        return bot.register_next_step_handler(message, check)
    elif message.text == f"Вернуться в меню {emojize(SMILE[1], use_aliases=True)}":
        bot.send_message(message.from_user.id,
                         "Вы в главном меню",
                         reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id,
                         "Такого варианта нет, попробуйте ещё раз",
                         reply_markup=keyboard)
    return bot.register_next_step_handler(message, main_menu)


@bot.callback_query_handler(func=lambda call: call.data.isdigit() or call.data in ["back", "next", "return", "delete",
                                                                                   "change_name", "change_date"])
def callback_worker(call):
    session = db_session.create_session()
    text = call.message.text.split("\n")
    try:
        now_page = int(text[0].split()[1])
    except Exception:
        pass
    if call.data == "back":
        if now_page - 1 >= 1:
            text[0] = f"Страница {now_page - 1} из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            for gg in range(1, 6):
                key_dict["1"][f"{(now_page - 2) * 5 + gg}"] = f"{(now_page - 2) * 5 + gg}"
            key_dict["1"][">"] = "next"
            list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(
                    f"{(now_page - 2) * 5 + 1 + i}. {list_poiska[5 * (now_page - 2) + i].name}\nДата: {list_poiska[5 * (now_page - 2) + i].time}")
            text = "\n".join(text)
        else:
            text[0] = f"Страница {int(text[0].split()[3])} из {int(text[0].split()[3])}"
            list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
            key_dict = {"1": {"<": "back"}}
            now_page = int(text[0].split()[3]) - 1
            for i in range((len(list_poiska) - 1) % 5 + 1):
                key_dict["1"][f"{now_page * 5 + 1 + i}"] = f"{now_page * 5 + 1 + i}"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range((len(list_poiska) - 1) % 5 + 1):
                text.append(
                    f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].name}\nДата: {list_poiska[5 * now_page + i].time}")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "next":
        list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
        now_page = int(text[0].split()[1])
        if now_page + 1 <= int(text[0].split()[3]):
            if now_page + 1 != int(text[0].split()[3]):
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                for gg in range(1, 6):
                    key_dict["1"][f"{now_page * 5 + gg}"] = f"{now_page * 5 + gg}"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].name}\nДате: {list_poiska[5 * now_page + i].time}")
                text = "\n".join(text)
            else:
                text[0] = f"Страница {now_page + 1} из {int(text[0].split()[3])}"
                key_dict = {"1": {"<": "back"}}
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    key_dict["1"][f"{now_page * 5 + i + 1}"] = f"{now_page * 5 + 1 + i}"
                key_dict["1"][">"] = "next"
                text = text[: 2]
                for i in range((len(list_poiska) - 1) % 5 + 1):
                    text.append(
                        f"{now_page * 5 + 1 + i}. {list_poiska[5 * now_page + i].name}\nДата: {list_poiska[5 * now_page + i].time}")
                text = "\n".join(text)
        else:
            text[0] = f"Страница 1 из {int(text[0].split()[3])}"
            key_dict = {"1": {"<": "back"}}
            for gg in range(1, 6):
                key_dict["1"][f"{gg}"] = f"{gg}"
            key_dict["1"][">"] = "next"
            text = text[: 2]
            for i in range(5 if len(list_poiska) >= 5 else len(list_poiska) % 5):
                text.append(f"{1 + i}. {list_poiska[i].name}\nДата: {list_poiska[i].time}")
            text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "return":
        session = db_session.create_session()
        list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
        key_dict = {"1": {}}
        if len(list_poiska) > 5:
            key_dict["1"]["<"] = "back"
        text = call.message.text.split("\n")
        nomer = int(text[0].split()[1][1:])
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            try:
                min_time = datetime.datetime.strptime(str(list_poiska[nomer1 * 5 + i].time), '%H:%M %d.%m.%Y')
            except Exception:
                min_time = datetime.datetime.fromtimestamp(float(list_poiska[nomer1 * 5 + i].time), timezone.utc)
            min_time = min_time.replace(tzinfo=pytz.utc)
            user = session.query(User).filter(User.tg_id == list_poiska[nomer1 * 5 + i].tg_id).first()
            min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
            string = f"{nomer1 * 5 + 1 + i}. {list_poiska[nomer1 * 5 + i].name}\nДата: {str(min_time).split('+')[0]}"
            text.append(string)
        text = "\n".join(text)
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            hz = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            key_dict["1"][f"{hz * 5 + i + 1}"] = f"{hz * 5 + i + 1}"
        if len(list_poiska) > 5:
            key_dict["1"][">"] = "next"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "delete":
        list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
        key_dict = {"1": {}}
        nomer = int(text[0].split()[1][1:])
        session.delete(list_poiska[nomer - 1])
        nomer -= 1
        if nomer <= 0:
            nomer = 1
        session.commit()
        list_poiska = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
        if len(list_poiska) > 5:
            key_dict["1"]["<"] = "back"
        text = call.message.text.split("\n")
        text = [
            f"Страница {nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1} из {len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1}",
            ""]
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            nomer1 = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            try:
                min_time = datetime.datetime.strptime(str(list_poiska[nomer1 * 5 + i].time), '%H:%M %d.%m.%Y')
            except Exception:
                min_time = datetime.datetime.fromtimestamp(float(list_poiska[nomer1 * 5 + i].time), timezone.utc)
            min_time = min_time.replace(tzinfo=pytz.utc)
            user = session.query(User).filter(User.tg_id == list_poiska[nomer1 * 5 + i].tg_id).first()
            min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
            string = f"{nomer1 * 5 + 1 + i}. {list_poiska[nomer1 * 5 + i].name}\nДата: {str(min_time).split('+')[0]}"
            text.append(string)
        text = "\n".join(text)
        for i in range((5 if (len(list_poiska) // 5 if len(list_poiska) % 5 == 0 else len(list_poiska) // 5 + 1) != (
                nomer // 5 if nomer % 5 == 0 else nomer // 5 + 1) else len(list_poiska) % 5) if len(
            list_poiska) != 5 else 5):
            hz = nomer // 5 - 1 if nomer % 5 == 0 else nomer // 5
            key_dict["1"][f"{hz * 5 + i + 1}"] = f"{hz * 5 + i + 1}"
        if len(list_poiska) > 5:
            key_dict["1"][">"] = "next"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons_creator(key_dict))
    elif call.data == "change_name":
        pass
    elif call.data == "change_date":
        pass
    elif call.data.isdigit():
        nomer = int(call.data)
        _list = session.query(Task).filter(Task.tg_id == call.message.chat.id).all()
        task = _list[nomer - 1]
        text = []
        text.append(f"Задача №{nomer}")
        text.append(f"Назавние: {task.name}")
        try:
            min_time = datetime.datetime.strptime(str(task.time), '%H:%M %d.%m.%Y')
        except Exception:
            min_time = datetime.datetime.fromtimestamp(float(task.time), timezone.utc)
        min_time = min_time.replace(tzinfo=pytz.utc)
        user = session.query(User).filter(User.tg_id == task.tg_id).first()
        min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
        text.append(f"Дата напоминания: {str(min_time).split('+')[0]}")
        user = session.query(User).filter(User.tg_id == task.tg_id).first()
        try:
            min_time = datetime.datetime.strptime(str(task.time), '%H:%M %d.%m.%Y')
        except Exception:
            min_time = datetime.datetime.fromtimestamp(float(task.time), timezone.utc)
        min_time = min_time.replace(tzinfo=pytz.utc)
        min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
        utcmoment_naive = datetime.datetime.utcnow()
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        time_now = utcmoment.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
        print(min_time, time_now, min_time - time_now)
        text.append(f"Осталось: {min_time - time_now}")
        buttons = buttons_creator({"1": {'Изменить название': 'change_name',
                                         'Изменить дату': 'change_date',
                                         f'{emojize(SMILE[2], use_aliases=True)}': "delete"},
                                   "2": {f"{emojize(SMILE[0], use_aliases=True)} Вернуться назад": 'return'}})
        text = "\n".join(text)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=buttons)


def check_tasks():
    session = db_session.create_session()
    tasks = session.query(Task).all()
    for task in tasks:
        try:
            user = session.query(User).filter(User.tg_id == task.tg_id).first()
            try:
                last_time = datetime.datetime.strptime(str(task.last_time), '%Y-%m-%d %H:%M:%S.%f%z')
            except Exception:
                last_time = datetime.datetime.fromtimestamp(float(task.last_time), timezone.utc)
            try:
                min_time = datetime.datetime.strptime(str(task.time), '%H:%M %d.%m.%Y')
            except Exception:
                min_time = datetime.datetime.fromtimestamp(float(task.time), timezone.utc)
            min_time = min_time.replace(tzinfo=pytz.utc)
            min_time = min_time.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
            utcmoment_naive = datetime.datetime.utcnow()
            utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
            time_now = utcmoment.astimezone(pytz.timezone(timezones[user.time_zone - 2]))
            text = []
            text.append(f"Название: {task.name}")
            text.append(f"Дата: {task.time}")
            text.append(f"Осталось: {min_time - time_now}")
            text = "\n".join(text)
            if (min_time - time_now).days >= 1 and (time_now - last_time).days >= 1 and (
                    (23 <= time_now.hour or time_now.hour <= 6) and user.night_writing or 6 < time_now.hour < 23):
                bot.send_message(task.tg_id, text)
                task.last_time = time_now
                session.commit()
            elif time_now > min_time:
                text = [f"Истекло время у напоминания:\n{task.name}\n", "Удачи"]
                text = "\n".join(text)
                bot.send_message(task.tg_id, text)
                bot.send_sticker(task.tg_id, 'CAACAgQAAxkBAAECtK1hD5nvhj5eh-MvUgWqT17iBCSitgACTgEAAqghIQaryAIOhrVIdyAE')
                session.delete(task)
                session.commit()
            elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 and (
                    time_now - last_time).seconds + (
                    time_now - last_time).days * 3600 * 24 >= 60 * 30 and (
                    (23 <= time_now.hour or time_now.hour <= 6) and user.night_writing or 6 < time_now.hour < 23):
                bot.send_message(task.tg_id, text)
                task.last_time = time_now
                session.commit()
            elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 * 5 and (
                    time_now - last_time).seconds + (
                    time_now - last_time).days * 3600 * 24 >= 60 * 60 and (
                    (23 <= time_now.hour or time_now.hour <= 6) and user.night_writing or 6 < time_now.hour < 23):
                bot.send_message(task.tg_id, text)
                task.last_time = time_now
                session.commit()
            elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 * 12 and (
                    time_now - last_time).seconds + (
                    time_now - last_time).days * 3600 * 24 >= 60 * 60 * 3 and (
                    (23 <= time_now.hour or time_now.hour <= 6) and user.night_writing or 6 < time_now.hour < 23):
                bot.send_message(task.tg_id, text)
                task.last_time = time_now
                session.commit()
            elif (min_time - time_now).days == 0 and (time_now - last_time).seconds + (
                    time_now - last_time).days * 3600 * 24 >= 60 * 60 * 6 and (
                    (23 <= time_now.hour or time_now.hour <= 6) and user.night_writing or 6 < time_now.hour < 23):
                bot.send_message(task.tg_id, text)
                task.last_time = time_now
                session.commit()
        except Exception as ex:
            print(ex)


def upload_bd():
    if yandex_disk.exists("my.sqlite"):
        yandex_disk.remove("my.sqlite")
    yandex_disk.upload("bd/my.sqlite", "my.sqlite")
    print("db uploaded")


def start_chek():
    schedule.every(30).seconds.do(check_tasks)
    schedule.every(5).minutes.do(upload_bd)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_tg_bot():
    for _ in range(10):
        try:
            print('\033[0mStarted.....')
            log()
            # bot.polling(none_stop=True)
            bot.infinity_polling()
        except Exception as err:
            print('\033[31mCrashed.....')
            print(f"Error: {err}")
            time.sleep(10)
            print('\033[35mRestarting.....')


try:
    x = threading.Thread(target=start_chek)
    x.start()
    x = threading.Thread(target=start_tg_bot)
    x.start()
except Exception:
    print('\033[35mОшибка, мы не смогли решить её.\033[0m')
