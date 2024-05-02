# ОПРОС СЕРВЕРА ДЛЯ ВЫЯСНЕНИЯ СТРУКТУРЫ ОТВЕТА С ПОМОШЬЮ ПРЯМОГО API

# import requests
# import time

# # fmt: off
# BOT_TOKEN = '6853999918:AAFO25k2gB3J-hedaMOXPcD8s6bRwHteqsI'
# API_URL = "https://api.telegram.org/bot"
# TEXT = "Ты написал мне! Не пиши, заебал"
# MAX_COUNTER = 100
# CATS_API = 'https://api.thecatapi.com/v1/images/search'
# # fmt: on

# offset = -2
# counter = 0
# chat_id: int

# while True:
#     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}').json()
#     print(updates)
#     if updates['result']:
#         if "text" in updates['result'][0]['message'] and updates['result'][0]['message']['text'] == 'end':
#             break
#         print(updates)
#         offset = updates['result'][0]['update_id']
#     time.sleep(1)

# ОПРОС СЕРВЕРА С ПОМОЩЬЮ АЙОГРАММ
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# create gile <Token.txt> and write into your token
BOT_TOKEN: str
with open("Token.txt") as f:
    BOT_TOKEN = f.read()

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text.lower() == "end")
async def process_end_polling(message: Message):
    await dp.stop_polling()


@dp.message()
async def process_check_message(message: Message):
    await message.send_copy(message.chat.id)
    print("-" * 40)
    print(message.model_dump_json(indent=4, exclude_none=True))


if __name__ == "__main__":
    dp.run_polling(bot)
