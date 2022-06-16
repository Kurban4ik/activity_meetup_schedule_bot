from aiogram import types

def poll_inline_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="+", callback_data="plus"),
        types.InlineKeyboardButton(text="-", callback_data="minus"),
        types.InlineKeyboardButton(text="Добавить друга", callback_data="add_friend"),
        types.InlineKeyboardButton(text="Удалить друга", callback_data="del_friend")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard