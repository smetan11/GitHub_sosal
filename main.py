import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import random
from markups import carapysKlava, carapysKlava2

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from states import carapys


bot = Bot(token="7763148917:AAEM-BDLxATH14zZZIR8So_kr5iMjcH3N4E")
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("привет я игровой бот", reply_markup=carapysKlava2)



@dp.callback_query(F.data.startswith("get point"))
async def cmd_start(message: types.Message, state: FSMContext):

    await message.answer("выберете уровень сложности", reply_markup=carapysKlava)
    await message.answer("игра началась")
    await message.answer("попоробуй угадать число от 1 до 100")
    a = random.randint(1, 100)
    await state.update_data(carapysNumber=a)
    await state.set_state(state=carapys.carapysVERI_HARD)


@dp.message(carapys.carapysVERI_HARD)
async def kaka(message: types.Message, state: FSMContext):
    data = await state.get_data()
    a = data.get('carapysNumber')
    if message.text == "lite":
        a = random.randint(1, 100)
        await state.update_data(carapysNumber=a, carapysMod="lite")
        await message.answer("ты  выбрал легкую сложность угадай число от 1 до 100")
        await state.set_state(carapys.carapysProwerka)
    if message.text == "medium":
        await message.answer("ты  выбрал нормальную сложность угадай число от 1 до 1000")
        a = random.randint(1, 1000)

        await state.update_data(carapysNumber=a,carapysMod="medium")



        await state.set_state(carapys.carapysProwerka)
    if message.text == "hard":
        await message.answer("ты  выбрал очень сложную сложность угадай число от 1 до 10000")
        a = random.randint(1, 10000)
        await state.update_data(carapysNumber=a, carapysMod="hard")
        await state.set_state(carapys.carapysProwerka)



async def main():
    await dp.start_polling(bot)


@dp.message(carapys.carapysProwerka)
async def one(message: types.Message, state: FSMContext):
    data = await state.get_data()
    a = data.get('carapysNumber')
    c1 = data.get("liteCount", 0 )
    c2 = data.get("mediumCount", 0 )
    c3 = data.get("hardCount", 0 )
    mode = data.get("carapysMod")
    if message.text.isdigit() and a == int(message.text):
        await message.answer("ты выйграл")
        await state.clear()
        if mode == "lite":
            c1 += 1
            await state.update_data(liteCount = c1   )
        elif mode == "medium":
            c2 += 1
            await state.update_data(mediumCount = c2)
        elif mode == "hard":
            c3 += 1
            await state.update_data(hardCount = c3)


    if a > int(message.text):
        await message.answer("попробуй побольше")
    if a < int(message.text):
        await message.answer("попробуй поменьше")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



