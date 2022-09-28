import gspread

from datetime import datetime
from settings import SheetsSecret, SheetsName, SheetPhones

import phonenumbers
from datetime import datetime

gc = gspread.service_account(filename=SheetsSecret)
sh = gc.open(SheetsName)
wks_phones = sh.worksheet(SheetPhones)

class PhonesClass():
    def _next_available_row(self):
        str_list = list(filter(None, wks_phones.col_values(1)))
        return str(len(str_list)+1)
    
    def if_user_not_registered(self, chat_id):
        chat_id = str(chat_id)
        cell = wks_phones.find(chat_id)
        return False if cell else True

    def save_user_telegram(self, chat_id, username):
        chat_id = str(chat_id)
        row     = self._next_available_row()
        id_col  = wks_phones.find('Id').col
        acc_col = wks_phones.find('Аккаунт').col
        wks_phones.update_cell(row, id_col, chat_id)
        wks_phones.update_cell(row, acc_col, username)
        print("\n{}: Registered new user {}".format(datetime.now(), chat_id))
    
    def if_user_has_to_set_name(self, chat_id):
        chat_id = str(chat_id)
        row = wks_phones.find(chat_id).row
        first_name_col = wks_phones.find('Имя').col
        last_name_col  = wks_phones.find('Фамилия').col
        first_name = wks_phones.cell(row, first_name_col).value
        last_name  = wks_phones.cell(row, last_name_col).value
        return first_name == None and last_name == None
    
    def get_user_firstname(self, chat_id):
        chat_id = str(chat_id)
        row = wks_phones.find(chat_id).row
        first_name_col = wks_phones.find('Имя').col
        first_name = wks_phones.cell(row, first_name_col).value
        return first_name

    def save_user_name(self, chat_id, first_name, last_name):
        chat_id = str(chat_id)
        row = wks_phones.find(chat_id).row
        first_name_col = wks_phones.find('Имя').col
        last_name_col  = wks_phones.find('Фамилия').col
        wks_phones.update_cell(row, first_name_col, first_name)
        wks_phones.update_cell(row, last_name_col, last_name)
        print("\n{}: Set name for user {}".format(datetime.now(), chat_id))
    
    def if_user_has_to_enter_phone(self, chat_id):
        chat_id = str(chat_id)
        row = wks_phones.find(chat_id).row
        first_name_col = wks_phones.find('Имя').col
        last_name_col  = wks_phones.find('Фамилия').col
        phone_col      = wks_phones.find('Телефон').col
        first_name = wks_phones.cell(row, first_name_col).value
        last_name  = wks_phones.cell(row, last_name_col).value
        phone      = wks_phones.cell(row, phone_col).value
        return first_name != None and last_name != None and phone == None

    def save_user_phone(self, chat_id, phone):
        chat_id = str(chat_id)
        row = wks_phones.find(chat_id).row
        phone_col = wks_phones.find('Телефон').col
        wks_phones.update_cell(row, phone_col, phone)
        print("\n{}: Set phone for user {}".format(datetime.now(), chat_id))
    
    def check_if_valid_phone(self, phone):
        try:
            x = phonenumbers.parse(phone, "RU")
        except:
            print("\n{}: Got invalid phone number {}".format(datetime.now(), phone))
            return False, ''
        if len(str(x.national_number)) != 10:
            print("\n{}: Got invalid length of phone number {}".format(datetime.now(), phone))
            return False, ''
        valid_number = "+{}{}".format(x.country_code, x.national_number)
        return True, valid_number

Phones = PhonesClass()