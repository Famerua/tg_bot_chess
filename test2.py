from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
import random

BOT_TOKEN = ""
URL_API = "https://api.telegram.org/bot"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
VAL: int

# offset = -2

# while True:

#     updates = requests.get(f"{URL_API}{BOT_TOKEN}/getUpdates?offset={offset+1}").json()

#     if updates["result"]:
#         print(updates)
#         for update in updates["result"]:
#             offset = update["update_id"]

#     time.sleep(1)


@dp.message(Command(commands=["start"]))
async def process_command_start(message: Message):
    global VAL
    VAL = random.randint(1, 100)
    await message.answer(f"I choose some number from 1 to 100. Try to find it!")


@dp.message(F.text)
async def process_text_message(message: Message):
    if message.text.isdigit() and float(message.text).is_integer():
        val = int(message.text)
        if val > VAL:
            await message.answer("My number is lower")
        elif val < VAL:
            await message.answer("My number is greater")
        else:
            await message.answer(f"YOU DID IT!\n My value was {VAL}")
            await message.answer(f"If you wanna play again, write me /start")
    else:
        await message.answer("Write interger number")
    print(message.model_dump_json(indent=4, exclude_none=True))
    print(f"VAL = {VAL}")


@dp.message()
async def process_any_message(message: Message):
    await message.reply("Write interger number")
    print(message.model_dump_json(indent=4, exclude_none=True))


if __name__ == "__main__":
    dp.run_polling(bot)
