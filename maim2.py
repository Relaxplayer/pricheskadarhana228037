import telebot
from telebot import types
import sqlite3
from google import genai

client = genai.Client(api_key="AIzaSyAymxnApTCTEPipqaX46TaO8sIagGn4rMM",http_options={'api_version': 'v1beta'})

bot = telebot.TeleBot("8793393597:AAGuv3AQfsw9IVbqmZizh8qmgnjStxEP-sc")

name = None

WebInfo1=types.WebAppInfo("https://kahoot.it/")
WebInfo2=types.WebAppInfo("https://www.blooket.com/")
WebInfo3=types.WebAppInfo("https://getaclass.ru/")
webInfo4=types.WebAppInfo("https://www.yaklass.ru/")

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('EduBot.db')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS school (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), password VARCHAR(50), role VARCHAR(50))")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Приветствую! Я бот для учебы. Введи свой ник для регистрации:")
    bot.register_next_step_handler(message, get_username)


def get_username(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}! Теперь введи пароль:")
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global password
    password = message.text.strip()
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("Ученик"))
    markup.row(types.KeyboardButton("Учитель"))
    markup.row(types.KeyboardButton("Администрация"))
    bot.send_message(message.chat.id, "Теперь выберите роль:", reply_markup=markup)
    bot.register_next_step_handler(message, role1)


def role1(message):
    role=message.text.strip()

    if role=="Ученик":

        conn=sqlite3.connect('EduBot.sqlite3')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO school (name, password,role ) VALUES (?,?,?)",(name,password,role))
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти в меню", callback_data="open_menu"))
        bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup)



    elif role =="Учитель":
        conn=sqlite3.connect('EduBot.sqlite3')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO school (name, password,role ) VALUES (?,?,?)",(name,password,role))
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти в меню", callback_data="open_menu_teacher"))
        bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup)

    elif role == "Администрация":
        conn=sqlite3.connect('EduBot.sqlite3')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO school (name, password,role ) VALUES (?,?,?)",(name,password,role))
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти в меню", callback_data="open_menu_admimistration"))
        bot.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup)




    elif role!="Ученик" or "Учитель" or "Администрация":
        bot.send_message(message.chat.id, "Такой роли нет")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "open_menu":
        bot.answer_callback_query(call.id)
        show_student_menu(call.message)
    elif call.data == "open_menu_teacher":
        bot.answer_callback_query(call.id)
        show_teacher_menu(call.message)
    elif call.data == "open_menu_admimistration":
        bot.answer_callback_query(call.id)
        show_administration_menu(call.message)




def show_administration_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btna1 = types.KeyboardButton("Верефикация")
    btna2 = types.KeyboardButton("Блокировка")
    btna3 = types.KeyboardButton("Смена роли")
    btna4 = types.KeyboardButton("Общая статистика")
    btna12 = types.KeyboardButton("Выгрузка отчетов")
    btna12 = types.KeyboardButton("Поиск по базе")
    btna13 = types.KeyboardButton("Редактор расписания")
    markup.row(btna1, btna2)
    markup.row(btna3, btna4)
    markup.row(btna12, btna13)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)

def show_teacher_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnt1 = types.KeyboardButton("Журнал")
    btnt2 = types.KeyboardButton("Задания Ученикам")
    btnt3 = types.KeyboardButton("Помощь учителю")
    btnt4 = types.KeyboardButton("Связь с учениками")
    btnt12 = types.KeyboardButton("Статистика классов")

    markup.row(btnt1, btnt2)
    markup.row(btnt3, btnt4)
    markup.row(btnt12)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)


def show_student_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Конспекты")
    btn2 = types.KeyboardButton("Задания")
    btn3 = types.KeyboardButton("Подготовка ЕНТ")
    btn4 = types.KeyboardButton("Связь с учителем")
    btn5 = types.KeyboardButton("Развивающие игры")
    btn6 = types.KeyboardButton("Оценки")
    btn12 = types.KeyboardButton("Статистика")

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn12)

    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)



@bot.message_handler(commands=['menu'])
def handle_menu(message):
    show_student_menu(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()

    if text == "Конспекты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("Математика"), types.KeyboardButton("Химия"))
        markup.row(types.KeyboardButton("История"), types.KeyboardButton("Английский язык"))
        bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)


    elif text in ["Математика", "Химия", "История", "Английский язык"]:
        bot.send_message(message.chat.id, f"По какой теме нужен конспект по предмету {text}? Напишите тему:")
        bot.register_next_step_handler(message, generate_ai_conspect, text)


    if text == "Задания":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("по математике"), types.KeyboardButton("по химии"))
        markup.row(types.KeyboardButton("по истории"), types.KeyboardButton("по английскому языку"))
        bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)

    elif text in ["по математике", "по химии", "по истории", "по английскому языку"]:
        bot.send_message(message.chat.id, f"Какие нужны задания {text}? Напишите тему:")
        bot.register_next_step_handler(message, missions, text)




    if text=="Развивающие игры":

        markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("Kahoot", web_app=WebInfo1))
        markup.row(types.KeyboardButton("Blooket", web_app=WebInfo2))
        markup.row(types.KeyboardButton("GetAclass", web_app=WebInfo3))
        markup.row(types.KeyboardButton("Yaclass", web_app=webInfo4))
        bot.send_message(message.chat.id, "Выберите:", reply_markup=markup)

    if text == "Связь с учителем":
        bot.send_message(message.chat.id, "введите имя и фамилию учителя")


    elif text == "Подготовка ЕНТ":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("Математика + Физика"), types.KeyboardButton("Математика + Информатика"), types.KeyboardButton("Математика + География"))
        markup.row(types.KeyboardButton("Биология + Химия"), types.KeyboardButton("Биология + География"))
        markup.row(types.KeyboardButton("Иностранный язык + Всемирная история"))
        markup.row(types.KeyboardButton("Всемирная история + Основы права"), types.KeyboardButton("Каз./Рус. язык + Каз./Рус. литература"))
        markup.row(types.KeyboardButton("Творческий экзамен"))
        bot.send_message(message.chat.id, "Выберите профиль:", reply_markup=markup)
        bot.register_next_step_handler(message, ent)



    if text == "Статистика":
        bot.send_message(message.chat.id,f"📝 ВАША КАРТОЧКА\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👤 Имя: {name}\n"
            f"🆔 Твой ID: {message.from_user.id}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n")




def ent(message):
    ent1 = message.text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Коспекты по профилю"))
    markup.row(types.KeyboardButton("Тестовые задания"))
    markup.row(types.KeyboardButton("Источники"))
    markup.row(types.KeyboardButton("Полезные советы"))
    bot.send_message(message.chat.id,f"что вам нужно по {ent1}?", reply_markup=markup)


def missions(message,subject):
    zadaniya = message.text.strip()
    waitingzada = bot.send_message(message.chat.id, "🤖 ИИ составляет задания. Пожалуйста, подождите...")

    try:
        prompt = f"Напиши краткий и полезный конспект для ученика. Предмет: {subject}, Тема: {zadaniya}. Используй жирный шрифт для терминов и списки."

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=waitingzada.message_id,
            text=response.text,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при генерации. Попробуйте позже.")
        print(f"Ошибка ИИ: {e}")








def generate_ai_conspect(message, subject):
    topic = message.text.strip()
    waiting = bot.send_message(message.chat.id, "🤖 ИИ составляет конспект. Пожалуйста, подождите...")

    try:
        prompt = f"Напиши краткий и полезный конспект для ученика. Предмет: {subject}, Тема: {topic}. Используй жирный шрифт для терминов и списки."

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=waiting.message_id,
            text=response.text,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при генерации. Попробуйте позже.")
        print(f"Ошибка ИИ: {e}")


# Запуск
if __name__ == "__main__":
    print("Бот запущен...")

    bot.polling(none_stop=True)