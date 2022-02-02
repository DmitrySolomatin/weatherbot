import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram.ext import CallbackContext, MessageHandler, Filters
from weather_json import get_weather, geo_weather, get_weather_5, geo_weather_5
# import psycopg2 not used
import os
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from telegram import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from models_2 import UserCoord

load_dotenv()
# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# connection to postgres database

engine = create_engine(os.getenv('APP_DATABASE_URL'))
conn = engine.connect()
Session = sessionmaker(engine)
s = Session()


def start_handler(update: Updater, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Hello!')
    update.message.reply_text("Type /help for instructions.")


def help_handler(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Write /weather city.\nCity is where you want to know daily weather forecast."
        "\nFor example, \n\t\t\t/weather Berlin\n\t\t\t/weather Kiev. \n"
        "/weather5 city. It's a 5 day forecast.\n"
        "/loc , to send your location to know coordinates.\n"
        "/geo, to know daily weather forecast by location.\n"
        "/geo5 , to know 5 day weather forecast by location.")


def temperature_handler(update, context):
    # check arguments as location name
    if context.args:
        loc = "".join(context.args)
        result = get_weather(loc)
        context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="/weather city\nWrite location name as a argument.")


def temperature_handler_5(update, context):
    # check arguments as location name
    if context.args:
        loc = "".join(context.args)
        result_5 = get_weather_5(loc)
        context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result_5))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="/weather5 city\nWrite location name as a argument.")


# location
def loc_send_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send your location.", reply_markup=send_button())


def send_button():
    keyboard = [[KeyboardButton(text='Send my location️', request_location=True)]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def commit_to_db(update, context):  # write to database
    chat_id = update.effective_chat.id
    lat = str(update.message.location.latitude)
    lon = str(update.message.location.longitude)
    name = update.message.from_user.first_name
    u_id = update.message.from_user.id
    usercoord = UserCoord(u_id=u_id, name=name, lat=lat, lon=lon)
    # check if already exists the same row in the database
    qr = s.query(exists().where(UserCoord.u_id == u_id, UserCoord.lat == lat, UserCoord.lon == lon)).scalar()
    try:
        if qr is False:
            s.add(usercoord)
            s.commit()
    finally:
        s.close()


# daily weather forecast
def geo_handler(update, context):
    chat_id = update.effective_chat.id
    name = update.message.from_user.first_name
    u_id = update.message.from_user.id
    try:
        loc = s.query(UserCoord.lat, UserCoord.lon).filter_by(u_id=u_id).limit(1).all()
        result = geo_weather(loc[0][1], loc[0][0])
    finally:
        s.close()
    context.bot.send_message(chat_id=chat_id, text='{}'.format(result))


# five day weather forecast
def geo_handler_5(update, context):
    chat_id = update.effective_chat.id
    u_id = update.message.from_user.id
    try:
        loc = s.query(UserCoord.lat, UserCoord.lon).filter_by(u_id=u_id).limit(1).all()
        result5 = geo_weather_5(loc[0][1], loc[0][0])
    finally:
        s.close()
    context.bot.send_message(chat_id=chat_id, text=result5)


def main():
    APP_TOKEN = os.getenv('APP_TOKEN')
    updater = Updater(APP_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("weather", temperature_handler))
    updater.dispatcher.add_handler(CommandHandler("weather5", temperature_handler_5))
    updater.dispatcher.add_handler(CommandHandler("loc", loc_send_handler))
    updater.dispatcher.add_handler(CommandHandler("geo", geo_handler))
    updater.dispatcher.add_handler(CommandHandler("geo5", geo_handler_5))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, commit_to_db))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
