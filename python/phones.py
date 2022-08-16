from ntpath import join
import pygsheets
import asyncio
import pandas as pd

from datetime import datetime
from settings import SheetsSecret, SheetsName, SheetPhones, UpdatePhonesTimeout

gc = pygsheets.authorize(service_file=SheetsSecret)
sh = gc.open(SheetsName)
wks_phones = sh.worksheet_by_title(SheetPhones)

class PhonesClass():
    def __init__(self) -> None:
        self.df = self.get_wks_df()
        print("\n{}: Initialized phones".format(datetime.now()))
        print(self.df)
    
    def get_wks_df(self):
        df = wks_phones.get_as_df()
        df = df.astype(str)
        return df

    async def update(self) -> None:
        while True:
            wks_phones.set_dataframe(self.df,(1,1))
            print("\n{}: Updated phones".format(datetime.now()))
            await asyncio.sleep(UpdatePhonesTimeout)
    
    def if_user_not_registered(self, chat_id):
        chat_id = str(chat_id)
        return self.df.loc[self.df['Id'] == chat_id].empty

    def save_user_telegram(self, chat_id, username):
        chat_id = str(chat_id)
        tmp_df = pd.DataFrame({
            'Id': chat_id,
            'Аккаунт': username,
            'Имя': '',
            'Фамилия': '',
            'Телефон': '',
        }, index=[0])
        self.df = pd.concat([self.df, tmp_df], ignore_index=True)
        print("\n{}: Registered new user {}".format(datetime.now(), chat_id))
    
    def if_user_has_to_set_name(self, chat_id):
        chat_id = str(chat_id)
        tmp_df = self.df.loc[
            (self.df['Id'] == chat_id) &
            (self.df['Имя'] == '') &
            (self.df['Фамилия'] == '')
        ]
        return not tmp_df.empty

    def save_user_name(self, chat_id, first_name, last_name):
        chat_id = str(chat_id)
        tmp_df = self.df.loc[self.df['Id'] == chat_id]
        tmp_df['Имя'] = first_name
        tmp_df['Фамилия'] = last_name
        self.df.update(tmp_df)
        print("\n{}: Set name for user {}".format(datetime.now(), chat_id))
    
    def if_user_has_to_enter_phone(self, chat_id):
        chat_id = str(chat_id)
        tmp_df = self.df.loc[
            (self.df['Id'] == chat_id) &
            (self.df['Имя'] != '') &
            (self.df['Фамилия'] != '') &
            (self.df['Телефон'] == '')
        ]
        return not tmp_df.empty

    def save_user_phone(self, chat_id, phone):
        chat_id = str(chat_id)
        tmp_df = self.df.loc[self.df['Id'] == chat_id]
        tmp_df['Телефон'] = phone
        self.df.update(tmp_df)
        print("\n{}: Set phone for user {}".format(datetime.now(), chat_id))

Phones = PhonesClass()