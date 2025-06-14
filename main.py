import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import random

from carapysBaza import init_db, update_score
from markups import carapysKlava, carapysKlava2

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from states import carapys
from carapysBaza import add_user
from carapysBaza import get_user

load_dotenv()

bot = Bot(token=os.getenv('token'))
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    if user is None:
        await add_user(str(message.from_user.id), username=message.from_user.username)

    await message.answer("привет я игровой бот", reply_markup=carapysKlava2)


@dp.callback_query(F.data.startswith("get_profile"))
async def send_profile(call: types.CallbackQuery, state: FSMContext):
    user = await get_user(str(call.from_user.id))
    await call.message.edit_text(f"{user.username} \n"
                                 f"победы: \n"
                                 f"легкие {user.lite_count} \n"
                                 f"среднии {user.medium_count} \n"
                                 f"сложные {user.hard_count}")


@dp.callback_query(F.data.startswith("get point"))
async def cmd_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("выберете уровень сложности", reply_markup=carapysKlava)
    a = random.randint(1, 100)
    await state.update_data(carapysNumber=a)
    await state.set_state(state=carapys.carapysVERI_HARD)


@dp.message(carapys.carapysVERI_HARD)
async def kaka(message: types.Message, state: FSMContext):
    if message.text == "lite":
        a = random.randint(1, 100)
        await state.update_data(carapysNumber=a, carapysMod="lite")
        await message.answer("ты  выбрал легкую сложность угадай число от 1 до 100")
        await state.set_state(carapys.carapysProwerka)
    if message.text == "medium":
        await message.answer("ты  выбрал нормальную сложность угадай число от 1 до 1000")
        a = random.randint(1, 1000)
        await state.update_data(carapysNumber=a, carapysMod="medium")
        await state.set_state(carapys.carapysProwerka)
    if message.text == "hard":
        await message.answer("ты  выбрал очень сложную сложность угадай число от 1 до 10000")
        a = random.randint(1, 10000)
        await state.update_data(carapysNumber=a, carapysMod="hard")
        await state.set_state(carapys.carapysProwerka)


async def on_startup():
    await init_db()
    logging.info('db ready')


async def main():
    await on_startup()
    await dp.start_polling(bot)


@dp.message(carapys.carapysProwerka)
async def one(message: types.Message, state: FSMContext):
    data = await state.get_data()
    a = data.get('carapysNumber')
    mode = data.get("carapysMod")
    if message.text.isdigit() and a == int(message.text):
        await message.answer("ты выйграл")
        await state.clear()
        await update_score(str(message.from_user.id), 1, mode)

    if a > int(message.text):
        await message.answer("попробуй побольше")
    if a < int(message.text):
        await message.answer("попробуй поменьше")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
