

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import sqlite3

# Установите уровень логирования (необязательно)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Состояния для конечного автомата (если нужно)
START, AWAITING_TEXT = range(2)

# Словарь для хранения заявок
applications = {}

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f"\U0001F47E: Привет, {user.first_name}! Я бот для сбора Анонимных заявок и комментариев."
                              " \n\n"
                              " Вы можете использовать команды:\n"
                              "/help - Общие команды бота (Развёрнутое описание)\n"
                            #   "/kng111 - Пример команды\n"
                              "/stop - Остановить взаимодействие\n"
                              "/coment - Оставить комментарий (Анонимно)\n"
                              "/primer - Пример заявки (Важно для конкурса)\n"
                              "/zayvka - Оставить заявку на конкурс\n\n"
                              )
    return AWAITING_TEXT

# Функция для обработки команды /kng111
def kng111(update: Update, context: CallbackContext) -> int:
    db = sqlite3.connect('sqlKon.db')
    cur = db.cursor()
    update.message.reply_text("secret code KNG111.")
    cur.execute('SELECT zayvki FROM zayv')
    result = cur.fetchall()
    update.message.reply_text(f"Заявок:{len(result)}")
    for i in range(len(result)):
        b = result[i]
        update.message.reply_text(f"Заявка:{(b)}")
    return AWAITING_TEXT

def kng222(update: Update, context: CallbackContext) -> int:
    db = sqlite3.connect('sqlKon.db')
    cur = db.cursor()
    update.message.reply_text("secret code KNG222.")
    cur.execute('SELECT comment FROM comm')
    result = cur.fetchall()
    update.message.reply_text(f"Комментариев:{len(result)}")
    for i in range(len(result)):
        b = result[i]
        update.message.reply_text(f"Комментарии:{(b)}")
    return AWAITING_TEXT

# Функция для обработки команды /stop
def stop(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вы прекратили взаимодействие с ботом.")
    return ConversationHandler.END

# Функция для обработки команды /coment
def coment(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text("Пожалуйста, напишите ваш комментарий.")


    # Помечаем, что пользователь находится в режиме ожидания ввода заявки
    context.user_data['waiting_for_comm'] = True
    
    return AWAITING_TEXT

# Функция для обработки команды /primer
def primer(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("\U0001F4E6 Заяка должна включать в себя:\n"
                              "ФИО: [ваше ФИО]\n"
                              "Группа: [номер вашей группы]\n"
                              "Tg: [ваш username]*Не обязательно\n"
                              "Текст заявки: [текст заявки] *до 1000 символов\n"
                            #   "*Заявки приходят Анонимно*\nчто бы в случае победы мы вас нашли укажите:Контактную информацию,ФИО,Группу\n")
                              "\nПример:\n\U0001F4ADЗдравствуйте, я бы хотел что бы в колледже реализовали/сделали/появилось [Ваша идея], я [фио] из группы [номер группы]\n"
                              "\n\U0001F947*Так же будет эффективно если вы раскажите подробнее о своей идеи и как её можно реализовать *\n"
                              "/zayvka - Оставить заявку на конкурс"
    )
    
    return AWAITING_TEXT

def help(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Команды:\n"
                            "/stop - Остановить взаимодействие\n"
                            "/coment - Оставить комментарий Анонимно, уточняйте что вы хотите рассказать, мы постараемся решить вашу проблему как можно эффективнее (о преподователи, о вашей паре, о ситуации в коллективе) \U0001F440\n"
                            "/primer - Пример заявки, пример как нужно заполнить заявку на конкурс заявок \U0001F4E6\n"
                            "/zayvka - Оставить заявку на конкурс, *сначала посмотрите пример заявки, что бы она не потерялась* \U0001F5D2\n\n")
    return AWAITING_TEXT


def zayvka(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text("Вы хотите оставить заявку. Пожалуйста, напишите вашу заявку (до 1000 символов).")

    # Помечаем, что пользователь находится в режиме ожидания ввода заявки
    context.user_data['waiting_for_zayvka'] = True
    
    return AWAITING_TEXT

# def stop_bot(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user

#     # Проверьте, что это сообщение отправлено администратором (или нужным пользователем)
#     if user.username == 'kng109':  # Замените 'YOUR_ADMIN_USERNAME' на имя вашего администратора
#         update.message.reply_text("Бот остановлен.")
#         update.stop()  # Остановите бота
#     else:
#         update.message.reply_text("У вас нет доступа к этой команде.")

# Функция для обработки текстовых сообщений (заявок)
def handle_text(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text
    
    # Проверяем, находится ли пользователь в режиме ожидания ввода заявки
    if context.user_data.get('waiting_for_zayvka', False):
        # Опционально, можно добавить проверку на длину текста заявки
        if len(text) > 1000:
            update.message.reply_text("\U0000274C\nЗаявка слишком длинная. Пожалуйста, укорьте текст до 1000 символов.")
        else:
            # Сохраняем заявку пользователя в базе данных
            db = sqlite3.connect('sqlKon.db')
            cursor = db.cursor()
            cursor.execute('INSERT or ignore INTO zayv (zayvki,userID) VALUES (?,?)', (text,user.username,))
            db.commit()
            db.close()

            update.message.reply_text(f"\U00002705\nЗаявка от {user.first_name} принята и сохранена в базе данных:\n\n{text}\n\n"
                                      "Спасибо за обращение!")
        
        # Выход из режима ожидания ввода заявки
        context.user_data['waiting_for_zayvka'] = False
    elif context.user_data.get('waiting_for_comm', False):
        if len(text) > 2000:
            update.message.reply_text("\U0000274C\nКомментарий слишком длинный. Пожалуйста, укорьте текст до 2000 символов.")
        else:
            # Сохраняем заявку пользователя в базе данных
            db = sqlite3.connect('sqlKon.db')
            cursor = db.cursor()
            cursor.execute('INSERT or ignore INTO comm (comment,userID) VALUES (?,?)', (text,user.username,))
            db.commit()
            db.close()

            update.message.reply_text(f"\U00002705\nКомментарий от {user.first_name} принят и сохранён в базе данных комментариев:\n\n{text}\n\n"
                                      "Спасибо за обращение!")
        
        # Выход из режима ожидания ввода заявки
        context.user_data['waiting_for_comm'] = False
    else:
        update.message.reply_text(f"\U00002049\nЯ не понимаю вас {user.first_name}\nвоспользуйтесь командами для обращения:\n/help или /start\n")
    
    return AWAITING_TEXT

# Функция для обработки неизвестных команд
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Извините, я не понимаю эту команду.\nНапишите сначала /start")

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    updater = Updater(token='6297955354:AAGN-1mDkpxFcviDRyZJ6qwuNj596zTCKhU', use_context=True)


    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AWAITING_TEXT: [MessageHandler(Filters.text & ~Filters.command, handle_text)],
        },
        fallbacks=[CommandHandler('start', start), CommandHandler('stop', stop), CommandHandler('coment', coment), CommandHandler('kng111', kng111), CommandHandler('primer', primer),CommandHandler("help", help) ],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('coment', coment))
    dp.add_handler(CommandHandler('kng111', kng111))
    dp.add_handler(CommandHandler('kng222', kng222))
    dp.add_handler(CommandHandler('primer', primer))
    dp.add_handler(CommandHandler('zayvka', zayvka))
    # dp.add_handler(CommandHandler('stopbotkingomoron1', stop_bot))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()