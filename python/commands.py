import pygsheets
import asyncio
import telebot

from datetime import datetime
from settings import SheetsSecret, SheetsName, SheetCommands, UpdateCommandsTimeout

gc = pygsheets.authorize(service_file=SheetsSecret)
sh = gc.open(SheetsName)
wks_commands = sh.worksheet_by_title(SheetCommands)

class CommandsClass():
    def __init__(self) -> None:
        self.valid = self._get_commands()
        print("\n{}: Initialized with commands".format(datetime.now()))
        print(self.valid)

    async def update_valid(self, bot) -> None:
        while True:
            self.valid = self._get_commands()
            print("\n{}: Updated commands".format(datetime.now()))
            print(self.valid)
            await self._set_to_bot(bot)
            await asyncio.sleep(UpdateCommandsTimeout)
    
    async def _set_to_bot(self, bot) -> None:
        await bot.set_my_commands(
            commands=[
                telebot.types.BotCommand(row['Команда'], row['Описание'])
                for _, row in self.valid.iterrows()
            ]
        )

    def _get_commands(self):
        all_commands = wks_commands.get_as_df()
        valid_commands = all_commands.loc[
            (all_commands['Команда'] != '') &
            (all_commands['Описание'] != '') &
            (all_commands['Текст'] != '')
        ]
        return valid_commands

    def get_valid_list(self):
        return self.valid['Команда'].values.tolist()
    
    def get_row_by_command(self, command):
        return self.valid.loc[self.valid['Команда'] == command].iloc[0]

Commands = CommandsClass()