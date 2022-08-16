from telebot.async_telebot import AsyncTeleBot

from datetime import datetime
from settings import BotToken

from keyboard import Keyboard
from phones import Phones
from phone_parser import check_if_valid_phone

Bot = AsyncTeleBot(BotToken, parse_mode='Markdown')

@Bot.message_handler(func=lambda m: Phones.if_user_not_registered(m.chat.id))
async def start_handler(message):
    await Bot.send_message(message.chat.id, """
Привет! Я - бот-путеводитель по ДОЛ Бауманец!
        
Введи свои *Фaмилию* и *Имя* через пробел.
    """)
    Phones.save_user_telegram(message.chat.id, message.chat.username)

@Bot.message_handler(func=lambda m: Phones.if_user_has_to_set_name(m.chat.id))
async def name_handler(message):
    name = message.text.split(' ')
    if (len(name) != 2):
        await Bot.send_message(message.chat.id, "Не похоже на *Фaмилию* и *Имя*\n\nПопробуй ещё раз")
        return

    first_name, last_name = name[1], name[0]
    Phones.save_user_name(message.chat.id, first_name, last_name)
    await Bot.send_message(message.chat.id, """
Супер! Привет, {}!

Теперь введи свой номер телефона.
    """.format(first_name))

@Bot.message_handler(func=lambda m: Phones.if_user_has_to_enter_phone(m.chat.id))
async def phone_handler(message):
    phone = message.text
    is_valid, valid_phone = check_if_valid_phone(phone)
    if is_valid == False:
        await Bot.send_message(message.chat.id, "Не похоже на номер телефона\n\nПопробуй ещё раз")
        return

    Phones.save_user_phone(message.chat.id, valid_phone)
    await Bot.send_message(message.chat.id, """
Ура! Ты зарегистрирован!

Нажми на кнопку *Меню* чтобы узнать побольше о нашем лагере!
    """,reply_markup=Keyboard.get_keyboard_markup())

@Bot.message_handler(func=lambda m: Keyboard.is_description_exists(m.text))
async def comands_handler(message):
    description = message.text
    df_reply = Keyboard.get_row_by_description(description)
    
    print("\n{}: Got description".format(datetime.now()))
    print(df_reply)
    
    description = df_reply['Описание']
    text = df_reply['Текст']
    await Bot.send_message(message.chat.id, description + '\n\n' + text, reply_markup=Keyboard.get_keyboard_markup())
    
    if df_reply['Изображение'] != '':
        image = df_reply['Изображение']
        await Bot.send_photo(message.chat.id, image, reply_markup=Keyboard.get_keyboard_markup() )