import os
from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext, MessageHandler, Filters
from weather_json import get_weather, geo_weather, get_weather_5, geo_weather_5
import os
import telegram
#from telegram import Update
from dotenv import load_dotenv
load_dotenv()

def start_handler(update:Updater, context:CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Hello!')
    update.message.reply_text("Type /help for instructions.")


def help_handler(update:Updater, context: CallbackContext):
    update.message.reply_text(
        "Write /temp city_name, city_name is a city where you want to know daily weather forecast."
        "\nFor example, \n\t\t/temp Berlin\n\t\t/temp Kiev. \n/geo \n"
        "To get daily weather forecast by your location coordinates.\n"
        "/temp5 city_name to know 5 day forecast.\n"
        "/geo5 5 day weather forecast by location coordinates")


def geo_text_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send your location.")

def geo_handler(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    result = geo_weather(lon, lat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def geo_text_handler_5(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Send your location.")

def geo_handler_5(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    result_5 = geo_weather_5(lon, lat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result_5)

def temperature_handler(update, context):
    # check arguments as location name
    if len(context.args) == 0:
        update.message.reply_text("/temp location_name\nMust has location name as a parameter.")

    loc = "".join(context.args)
    result = get_weather(loc)
    update.message.reply_text("".join(result))

def temperature_handler_5(update, context):
    # check arguments as location name
    if len(context.args) == 0:
        update.message.reply_text("/temp5 location_name\nMust has location name as a parameter.")

    loc = "".join(context.args)
    result_5 = get_weather_5(loc)
    update.message.reply_text("".join(result_5))

def main():
    APP_TOKEN = os.getenv('APP_TOKEN')
    updater = Updater(APP_TOKEN ,use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("temp", temperature_handler))
    updater.dispatcher.add_handler(CommandHandler("temp5", temperature_handler_5))
    updater.dispatcher.add_handler(CommandHandler("geo", geo_text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, geo_handler))
    updater.dispatcher.add_handler(CommandHandler("geo5", geo_text_handler_5))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, geo_handler_5))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
