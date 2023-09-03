from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Определение состояний
START, AWAITING_INPUT = range(2)

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет! Я готов к работе. Отправьте /awaitinput, чтобы перейти в режим ожидания сообщений.")
    return START

# Функция для команды /awaitinput
def await_input(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Теперь я ожидаю вашего сообщения.")
    return AWAITING_INPUT

# Функция для обработки сообщений в режиме ожидания
def handle_input(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if user.username == "kng109":
        user_message = update.message.text
        update.message.reply_text(f"Вы написали: {user_message}")
        return START  # После обработки сообщения переходим обратно в начальное состояние
    else:
        update.message.reply_text(f"Бот выключен:")
        return AWAITING_INPUT

def main():
    updater = Updater(token='6297955354:AAGN-1mDkpxFcviDRyZJ6qwuNj596zTCKhU', use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [],
            AWAITING_INPUT: [MessageHandler(Filters.text & ~Filters.command, handle_input)],
        },
        fallbacks=[CommandHandler('awaitinput', await_input)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
