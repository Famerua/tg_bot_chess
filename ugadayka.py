from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dataclasses import dataclass
from random import randint


@dataclass
class User:
    in_game: bool = False
    secret_number: int = None
    attempts: int = None
    total_games: int = 0
    wins: int = 0


user = User()


def get_random_number():
    return randint(1, 100)


# create gile <Token.txt> and write into your token
BOT_TOKEN: str
with open("Token.txt") as f:
    BOT_TOKEN = f.read()

ATTEMPTS = 5

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        "Hello! Guess the number which i chosen! Lets play?\n\nTo see the rules send /help"
    )


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(
        "Game rules:\n I am guessing some number\n"
        f"Try to guess it in {ATTEMPTS} times\n\n"
        "Accesable commands:\n"
        "/help - see all rules"
        "/start - start game"
        "/stat - see your stat"
        "/cancel - stop playing"
    )


@dp.message(Command(commands=["stat"]))
async def process_stat_command(message: Message):
    await message.answer(
        f"Total games = {user.total_games}\n" f"Won games = {user.wins}"
    )


@dp.message(Command(commands=["cancel"]))
async def process_cancel_command(message: Message):
    if user.in_game:
        user.in_game = False
        await message.answer("You left game, pussy! If you wanna play again, write me")
    else:
        await message.answer("We didn't play\n Maybe let's play?")


@dp.message(F.text.lower().in_(["yes", "play", "go", "да", "давай", "хочу"]))
async def process_positive_answer(message: Message):
    if not user.in_game:
        user.in_game = True
        user.secret_number = get_random_number()
        user.attempts = ATTEMPTS
        await message.answer(
            f"Cool! I guessed number from 1 to 100. Try to find it in {ATTEMPTS} attempts!"
        )
    else:
        await message.answer("We are playing now! Send me numbers)")


@dp.message(F.text.lower().in_(["stop", "no", "нет", "хватит", "стоп", "не хочу"]))
async def process_negative_answer(message: Message):
    if not user.in_game:
        await message.answer("I am not glad to hear it. But ok :(")
    else:
        await message.answer("We must to finish game! I now your IP")


@dp.message(lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_num_answer(message: Message):
    if user.in_game:
        if int(message.text) == user.secret_number:
            user.in_game = False
            user.total_games += 1
            user.wins += 1
            await message.answer(
                f"Congratalates! You guessed number! It was {user.secret_number}"
            )
        elif int(message.text) > user.secret_number:
            user.attempts -= 1
            await message.answer("My number is lower")
        elif int(message.text) < user.secret_number:
            user.attempts -= 1
            await message.answer("My number is greater")

        if user.attempts == 0:
            user.in_game = False
            user.total_games += 1
            await message.answer(
                "You lose! You dont have attempts!\n"
                f"My number was {user.secret_number}\n"
                "Play one more?"
            )
    else:
        await message.answer("We are not playing now! Do you want?")


@dp.message()
async def process_another_answer(message: Message):
    if user.in_game:
        await message.answer(
            "We are playing now! Lets finish. Send me numbers from 1 to 100"
        )
    else:
        await message.answer("I dont understand you!")


if __name__ == "__main__":
    dp.run_polling(bot)
