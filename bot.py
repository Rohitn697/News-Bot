import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update,ReplyKeyboardMarkup
from utils import get_reply,fetch_news,topics_keyboard


logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1516125370:AAGD-5iqmovNloemjMOMkSGUhgv9UgX2kzg"


#webhook-----------------
app = Flask(__name__)

@app.route('/')
def index():
	return "hello!"

@app.route(f'/{TOKEN}' , methods=['GET','POST'])
def webhook():
	'''webhook view which recieves updates from telegram'''
	# create update object from json-format request data
	update = Update.de_json(request.get_json(),bot)
	#process update
	dp.process_update(update)
	return "ok"

#------------------------



def start(bot,update):
    print(update)
    author = update.message.from_user.first_name
    reply = "Hello! {}".format(author)
    bot.send_message(chat_id = update.message.chat_id, text = reply)

def _help(bot,update):
    helptxt = "Hey Welcome to help section"
    bot.send_message(chat_id = update.message.chat_id, text = helptxt)


def news(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def reply_text(bot, update):

    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "Get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)


def echo_sticker(bot,update):

    bot.send_sticker(chat_id = update.message.chat_id,
    sticker = update.message.sticker.file_id)


def error(bot,update):
    logger.error("Update: '%s' caused error '%s' ",update, update.error)




bot = Bot(TOKEN)
# handle multiple requests
try:
    bot.set_webhook("https://c0f9d921d158.ngrok.io/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot , None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
        app.run(port=8443)
