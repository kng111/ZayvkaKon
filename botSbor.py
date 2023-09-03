

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

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
                              "/primer - Пример заявки (Важно для конкурса)"
                              "/zayvka - Оставить заявку на конкурс\n\n"
                              )
    return AWAITING_TEXT

# Функция для обработки команды /kng111
def kng111(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Пример команды /kng111: это ваша заявка по курсу KNG111.")
    return AWAITING_TEXT

# Функция для обработки команды /stop
def stop(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вы прекратили взаимодействие с ботом.")
    return ConversationHandler.END

# Функция для обработки команды /coment
def coment(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Вы хотите оставить комментарий к заявке. Пожалуйста, напишите ваш комментарий.")
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
    update.message.reply_text("Это пример заявки:\n"
                            "/stop - Остановить взаимодействие\n"
                            "/coment - Оставить комментарий Анонимно, уточняйте что вы хотите рассказать, мы постараемся решить вашу проблему как можно эффективнее (о преподователи, о вашей паре, о ситуации в коллективе) \U0001F440\n"
                            "/primer - Пример заявки, пример как нужно заполнить заявку на конкурс заявок \U0001F4E6\n"
                            "/zayvka - Оставить заявку на конкурс, *сначала посмотрите пример заявки, что бы она не потерялась* \U0001F5D2\n\n")
    return AWAITING_TEXT

# Функция для обработки текстовых сообщений (заявок)
def handle_text(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text
    applications[user.id] = text  # Сохраняем заявку пользователя

    update.message.reply_text(f"{user.first_name} воспользуйтесь командами для обращения:\n/help или /start\n"
                              )
    # {text} - сообщение пользователя 
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
    dp.add_handler(CommandHandler('primer', primer))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
