import asyncio

from bot import Bot
from commands import Commands
from phones import Phones

loop = asyncio.get_event_loop()
asyncio.ensure_future(Commands.update_valid(Bot))
asyncio.ensure_future(Phones.update())
asyncio.ensure_future(Bot.polling(non_stop=True))
loop.run_forever()