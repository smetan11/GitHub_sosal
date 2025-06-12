from aiogram import types

carapysKnopka1 = types.KeyboardButton(text="lite")
carapysKnopka2 = types.KeyboardButton(text="medium")
carapysKnopka3 = types.KeyboardButton(text="hard")

carapysKlava = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[carapysKnopka1], [carapysKnopka2], [carapysKnopka3]])

carapysProfile = types.InlineKeyboardButton(text="профиль", callback_data="get_profile")
play = types.InlineKeyboardButton(text="игра", callback_data="get point")
carapysKlava2 = types.InlineKeyboardMarkup(inline_keyboard=[[carapysProfile, play]])
