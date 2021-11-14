import telebot

from telebot import types
from constants import API_KEY

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "Hello, {0.first_name}!".format(message.from_user) + "!", reply_markup = markup)
    return request_message(message)


@bot.message_handler(commands=['request'])
def request_message(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('ask')
    item2 = types.KeyboardButton('answer')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Please choose what you want to do next." , reply_markup = markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':

        if message.text == 'ask':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('math')
            item2 = types.KeyboardButton('programming')
            back = types.KeyboardButton('back')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, "You have selected the 'ask' command. Now, please select the area where you want to ask your question.", reply_markup=markup)

        elif message.text == 'answer':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('math')
            item2 = types.KeyboardButton('programming')
            back = types.KeyboardButton('back')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, "You have selected the 'answer' command. Now select the area where you want to answer someone's question.", reply_markup=markup)

        elif message.text == 'back':
            return find(message)

        elif  message.text == 'math':
            return find(message)



        elif message.text == 'programming':
            bot.send_message(message.chat.id, " ")
            return find(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, """
    The following commands are available:

    /start -> Welcome Message
    /help -> This Message
    /request -> Choose what to do
    """)

users = {}
freeid = None


@bot.message_handler(content_types=['text'])
def find(message: types.Message):
    global freeid

    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'Finding...')

        if freeid == None:
            freeid = message.chat.id
        else:
            bot.send_message(message.chat.id, 'Founded! Now formulate your question and send it here.')
            bot.send_message(freeid, 'Founded! Please wait till the user writes you the question.')

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None

        print(users, freeid)
    else:
        bot.send_message(message.chat.id, 'Sorry, we need some time to process.')


@bot.message_handler(commands=['stop'])
def stop(message: types.Message):
    global freeid

    if message.chat.id in users:
        bot.send_message(message.chat.id, 'Stopping...')
        bot.send_message(users[message.chat.id], 'Your opponent is leavin`...')

        del users[users[message.chat.id]]
        del users[message.chat.id]

        print(users, freeid)  # Debug purpose, you can remove that line
    elif message.chat.id == freeid:
        bot.send_message(message.chat.id, 'Stopping...')
        freeid = None

        print(users, freeid)  # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'You are not in search!')

@bot.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
    if message.chat.id in users:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)
    else:
        bot.send_message(message.chat.id, 'No one can hear you...')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    bot.send_message(message.chat.id, "I don't understand \"" + message.text + "\"\nMaybe try the help page at /help")


bot.infinity_polling(skip_pending=True)
