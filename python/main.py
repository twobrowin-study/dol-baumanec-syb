import asyncio

from bot import Bot
from keyboard import Keyboard
from phones import Phones

loop = asyncio.get_event_loop()
asyncio.ensure_future(Keyboard.update_valid())
asyncio.ensure_future(Phones.update())
asyncio.ensure_future(Bot.polling(non_stop=True))
loop.run_forever()