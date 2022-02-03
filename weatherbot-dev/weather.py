import os
from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, MessageHandler, Filters
from weather_json import get_weather, geo_weather, get_weather_5
import os
import telegram
import logging
from dotenv import load_dotenv

load_dotenv()

#logging
logging.basicConfig(
    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
logger = logging.getLogger(__name__)

def start_handler(update:Updater, context:CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Hello!')
    update.message.reply_text("Type /help for instructions.")


def help_handler(update, context: CallbackContext):
    update.message.reply_text(
        "Write /weather city.\nCity is where you want to know daily weather forecast."
        "\nFor example, \n\t\t\t/weather Berlin\n\t\t\t/weather Kiev. \n"
        "/weather5 city. It's a 5 day weather forecast.\n"
        "/geo, to know daily weather forecast by location.\n"
    )

def geo_text_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send your location.")

def geo_handler(update, context): #command geo
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    result = geo_weather(lon, lat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def temperature_handler(update, context): #command weather
    if context.args:
        loc = "".join(context.args)
        result = get_weather(loc)
        context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="/weather city\nWrite city name as a argument.")

def temperature_handler_5(update, context): #command weather5
    if context.args:
        loc = "".join(context.args)
        result_5 = get_weather_5(loc)
        context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result_5))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="/weather5 city\nWrite city name as a argument.")

def main():
    APP_TOKEN = os.getenv('APP_TOKEN')
    updater = Updater(APP_TOKEN ,use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("weather", temperature_handler))
    updater.dispatcher.add_handler(CommandHandler("weather5", temperature_handler_5))
    updater.dispatcher.add_handler(CommandHandler("geo", geo_text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, geo_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
