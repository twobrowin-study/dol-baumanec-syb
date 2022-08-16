from xmlrpc.client import Boolean
import phonenumbers
from datetime import datetime

def check_if_valid_phone(phone):
    try:
        x = phonenumbers.parse(phone, "RU")
    except:
        print("\n{}: Got invalid phone number {}".format(datetime.now(), phone))
        return False, ''
    valid_number = "+{}{}".format(x.country_code, x.national_number)
    return True, valid_number