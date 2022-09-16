import asyncio
import traceback

from bot import Bot
from keyboard import Keyboard
from phones import Phones

async def bot_restart_sequence():
    while True:
        try:
            await Bot.infinity_polling()
        except asyncio.CancelledError:
            # don't interfere with cancellations
            raise
        except Exception:
            print("Caught exception")
            traceback.print_exc()

async def main():
    await asyncio.gather(
        Keyboard.update_valid(),
        Phones.update(),
        bot_restart_sequence()
    )

if __name__ == '__main__':
    asyncio.run(main())