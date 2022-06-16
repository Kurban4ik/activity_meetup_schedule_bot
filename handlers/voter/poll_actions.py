from aiogram import types
from aiogram.utils import markdown

from loader import dp, bot, user_memory, user_friends_memory
from keyboards.inline.fb_vote_poll import poll_inline_keyboard
from markup.poll_text import TEXT_MSG

@dp.callback_query_handler(text="plus")
async def list_plus_user(call: types.CallbackQuery):

    post_keyboard = poll_inline_keyboard()
    message = call.message

    if call.from_user.id in user_memory:
        await bot.answer_callback_query(
            call.id,
            text='Вы уже в списке!', 
            show_alert=True)
    else:
        user_memory[call.from_user.id] = call.from_user
        answer = update_msg_text()
        await bot.edit_message_text(
            answer, 
            chat_id=message.chat.id, 
            message_id=message.message_id,
            reply_markup=post_keyboard,
            parse_mode='Markdown'
        )

@dp.callback_query_handler(text="minus")
async def list_minus_user(call: types.CallbackQuery):

    post_keyboard = poll_inline_keyboard()
    message = call.message

    if call.from_user.id not in user_memory:
        await bot.answer_callback_query(
            call.id,
            text='Вас нет в списке!', 
            show_alert=True)
    else:
        user_memory.pop(call.from_user.id)
        answer = update_msg_text()
        await bot.edit_message_text(
            answer, 
            chat_id=message.chat.id, 
            message_id=message.message_id,
            reply_markup=post_keyboard,
            parse_mode='Markdown'
        )

@dp.callback_query_handler(text="add_friend")
async def add_friend_to_list(call: types.CallbackQuery):
    post_keyboard = poll_inline_keyboard()
    message = call.message


    if user_friends_memory[call.from_user.id] < 3:
        user_friends_memory[call.from_user.id] += 1
        user_friend_counter = user_friends_memory[call.from_user.id]

        # ATTENTION user_id is usually int, but this is str
        user_id = f'{call.from_user.id}+{user_friend_counter}'

        user = call.from_user
        user.username = f'{user.username or ""} + Friend {user_friend_counter}'
        user_memory[user_id] = user

        answer = update_msg_text()
        await bot.edit_message_text(
            answer, 
            chat_id=message.chat.id, 
            message_id=message.message_id,
            reply_markup=post_keyboard,
            parse_mode='Markdown'
        )
    else:
        await bot.answer_callback_query(
            call.id,
            text='Вы можете добавить не больше троих!', 
            show_alert=True
            )

@dp.callback_query_handler(text="del_friend")
async def del_friend_from_list(call: types.CallbackQuery):
    post_keyboard = poll_inline_keyboard()
    message = call.message

    user_friend_counter = user_friends_memory[call.from_user.id]
    if user_friend_counter > 0:
        user_id = f'{call.from_user.id}+{user_friend_counter}'
        user_memory.pop(user_id)
        user_friends_memory[call.from_user.id] -= 1

        answer = update_msg_text()
        await bot.edit_message_text(
            answer, 
            chat_id=message.chat.id, 
            message_id=message.message_id,
            reply_markup=post_keyboard,
            parse_mode='Markdown'
        )
    else:
        await bot.answer_callback_query(
            call.id,
            text='Друзей в списке нет!', 
            show_alert=True
            )

def update_msg_text():
    HEADER = f'{TEXT_MSG}\nСписок игроков:\n'
    # user = list of users
    users = [f'{i+1}. [{user.first_name} {user.last_name or ""}](tg://user?id={user.id}) | {markdown.escape_md(user.username) or ""}' for i, user in enumerate(user_memory.values())]
    
    return HEADER + '\n'.join(users)
