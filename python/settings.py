from os import environ, getenv

BotToken = environ.get('BOT_TOKEN')
if BotToken == '' or BotToken == None:
    with open('telegram.txt', 'r') as fp:
        BotToken = fp.read()

SheetsAccJson = environ.get('SHEETS_ACC_JSON')
SheetsSecret = './serviceacc.json'
if SheetsAccJson != None and SheetsAccJson != '':
    with open(SheetsSecret, 'w') as fp:
        fp.write(SheetsAccJson)

SheetsName = getenv('SHEETS_NAME', 'Таблица бота бауманец для ШМБ')

SheetPhones = getenv('SHAEET_PHONE', 'Номера телефонов')
SheetKeyboard = getenv('SHEET_KEYBOARD', 'Команды бота')

UpdateKeyboardTimeout = int(getenv('UPDATE_KEYBOARD_TIMEOUT', 10))
UpdatePhonesTimeout = int(getenv('UPDATE_PHONES_TIMEOUT', 1))