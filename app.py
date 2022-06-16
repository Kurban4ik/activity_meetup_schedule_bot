from aiogram import executor, types, utils
import aioschedule
import asyncio

import handlers
from loader import dp, bot, post_memory, config, clear_memory
from markup.poll_text import TEXT_MSG
from keyboards.inline.fb_vote_poll import poll_inline_keyboard
from keyboards.reply.start_cmd_layout import start_cmd_keyboard

MY_CHANNEL = config['tg_channel']

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    answer_keyboard = start_cmd_keyboard()
    await message.answer("Choose start option", reply_markup=answer_keyboard)


@dp.message_handler(commands="delete_all_posts")
async def delete_posts(message: types.Message):
    for post_id in post_memory:
        try:
            await bot.delete_message(MY_CHANNEL, post_id)
            await message.answer("Successfully deleted the last post")
        except utils.exceptions.MessageToDeleteNotFound:
            await message.answer(f"Post {post_id} was more then 48H ago... You should delete post manually.")
    if not post_memory: 
        await message.answer("No post to delete from history(memory)")
    clear_memory()

# Хэндлер на команду /start_wednesday
@dp.message_handler(commands="start_wednesday")
async def start_poll_wednesday(message: types.Message):
    clear_memory()
    post_keyboard = poll_inline_keyboard()
    message_sent = await bot.send_message(MY_CHANNEL, TEXT_MSG, reply_markup=post_keyboard)
    post_memory.append(message_sent.message_id)

# Хэндлер на команду /start_wednesday
@dp.message_handler(commands="start_sunday")
async def start_poll_sunday(message: types.Message):
    clear_memory()
    post_keyboard = poll_inline_keyboard()
    message_sent = await bot.send_message(MY_CHANNEL, TEXT_MSG, reply_markup=post_keyboard)
    post_memory.append(message_sent.message_id)

# запуск по расписанию 
async def start_poll_scheduled():
    clear_memory()
    # постим опрос
    post_keyboard = poll_inline_keyboard()
    message_sent = await bot.send_message(MY_CHANNEL, TEXT_MSG, reply_markup=post_keyboard)
    post_memory.append(message_sent.message_id)

async def delete_last_posts():
    for post_id in post_memory:
        await bot.delete_message(MY_CHANNEL, post_id)
    clear_memory()


async def scheduler():
    # время по UTC 0 (Москва +3h)
    # Wednesday Poll (start, clearing)
    aioschedule.every().tuesday.at("07:00").do(start_poll_scheduled)
    aioschedule.every().thursday.at("06:30").do(delete_last_posts)
    # Sunday Poll (start, clearing)
    aioschedule.every().friday.at("08:00").do(start_poll_scheduled)
    aioschedule.every().sunday.at("07:30").do(delete_last_posts)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(dp):
    asyncio.create_task(scheduler())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
