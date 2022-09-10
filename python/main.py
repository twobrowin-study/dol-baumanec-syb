import asyncio

from bot import Bot
from keyboard import Keyboard
from phones import Phones

async def main():
    await asyncio.gather(
        Keyboard.update_valid(),
        Phones.update(),
        Bot.infinity_polling()
    )

if __name__ == '__main__':
    asyncio.run(main())