from telegram import Update, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import MessageFilter, ALL

from settings import BotToken

from keyboard import Keyboard
from phones import Phones

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown("""
Привет! Я - бот-путеводитель по ДОЛ Бауманец!
        
Введи свои *Фaмилию* и *Имя* через пробел.
    """)
    Phones.save_user_telegram(update.effective_user.id, update.effective_user.username)

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.message.text.split(' ')
    if (len(name) != 2):
        await update.message.reply_markdown("Не похоже на *Фaмилию* и *Имя*\n\nПопробуй ещё раз")
        return

    first_name, last_name = name[1], name[0]
    Phones.save_user_name(update.effective_user.id, first_name, last_name)
    await update.message.reply_markdown(f"""
Супер! Привет, {first_name}!

Теперь введи свой номер телефона.
    """)

async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phone = update.message.text
    is_valid, valid_phone = Phones.check_if_valid_phone(phone)
    if is_valid == False:
        await update.message.reply_markdown("Не похоже на номер телефона\n\nПопробуй ещё раз")
        return

    Phones.save_user_phone(update.effective_user.id, valid_phone)
    await update.message.reply_markdown("""
Ура! Ты зарегистрирован!

Нажми на одну из кнопок ниже чтобы узнать побольше о нашем лагере!
    """, reply_markup = Keyboard.get_keyboard_markup())

async def description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    description = update.message.text
    df_reply = Keyboard.get_row_by_description(description)
    
    description = df_reply['Описание']
    text = df_reply['Текст']
    await update.message.reply_markdown(description + '\n\n' + text, reply_markup=Keyboard.get_keyboard_markup())
    
    if df_reply['Изображение'] != '':
        image = df_reply['Изображение']
        await update.message.reply_photo(image, reply_markup=Keyboard.get_keyboard_markup())

async def etc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = Phones.get_user_firstname(update.effective_user.id)
    await update.message.reply_markdown(f"""
Привет, {first_name}! Ты уже зарегистрирован!

И, честно признаться, я тебя не понял...

Введи одну из следующих команд чтобы продолжить
""", reply_markup=Keyboard.get_keyboard_markup())

class UserNotRegistered(MessageFilter):
    def filter(self, message: Message) -> bool:
        return Phones.if_user_not_registered(message.chat_id)

class UserHasToSetName(MessageFilter):
    def filter(self, message: Message) -> bool:
        return Phones.if_user_has_to_set_name(message.chat_id)

class UserHasToEnterPhone(MessageFilter):
    def filter(self, message: Message) -> bool:
        return Phones.if_user_has_to_enter_phone(message.chat_id)

class IsDescriptionExists(MessageFilter):
    def filter(self, message: Message) -> bool:
        return Keyboard.is_description_exists(message.text)

Bot = ApplicationBuilder().token(BotToken).build()
Bot.add_handler(CommandHandler("start", start_handler, filters = UserNotRegistered()))
Bot.add_handler(CommandHandler("start", etc_handler))
Bot.add_handler(MessageHandler(ALL & UserNotRegistered(), start_handler))
Bot.add_handler(MessageHandler(ALL & UserHasToSetName(), name_handler))
Bot.add_handler(MessageHandler(ALL & UserHasToEnterPhone(), phone_handler))
Bot.add_handler(MessageHandler(ALL & IsDescriptionExists(), description_handler))
Bot.add_handler(MessageHandler(ALL, etc_handler))