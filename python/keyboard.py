import pygsheets
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from datetime import datetime
from settings import SheetsSecret, SheetsName, SheetKeyboard, UpdateKeyboardTimeout

gc = pygsheets.authorize(service_file=SheetsSecret)
sh = gc.open(SheetsName)
wks_keyboard = sh.worksheet_by_title(SheetKeyboard)

class KeyboardClass():
    def __init__(self) -> None:
        self.valid = self._get_keyboard_df()
        print("\n{}: Initialized with keyboard df".format(datetime.now()))
        print(self.valid)

    async def update_valid(self) -> None:
        while True:
            self.valid = self._get_keyboard_df()
            print("\n{}: Updated keyboard df".format(datetime.now()))
            print(self.valid)
            await asyncio.sleep(UpdateKeyboardTimeout)

    def _get_keyboard_df(self):
        all_keyboard = wks_keyboard.get_as_df()
        valid_keyboard = all_keyboard.loc[
            (all_keyboard['Описание'] != '') &
            (all_keyboard['Текст'] != '')
        ]
        return valid_keyboard

    def is_description_exists(self, description):
        df_tmp = self.valid.loc[self.valid['Описание'] == description]
        return not df_tmp.empty

    def get_row_by_description(self, description):
        return self.valid.loc[self.valid['Описание'] == description].iloc[0]
    
    def get_keyboard_markup(self):
        markup = ReplyKeyboardMarkup(row_width=2)
        nrows = self.valid.shape[0]
        for idx in range(0,nrows,2):
            desriptions = self.valid.iloc[idx:idx+2]['Описание'].values
            row = [KeyboardButton(x) for x in desriptions]
            markup.add(*row)
        return markup

Keyboard = KeyboardClass()