from aiogram import types

def start_cmd_keyboard() -> types.ReplyKeyboardMarkup:
    buttons = [
        types.KeyboardButton(text="/start_wednesday"),
        types.KeyboardButton(text="/start_sunday"),
        types.KeyboardButton(text='/delete_all_posts')
    ]
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard