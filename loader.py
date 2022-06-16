import logging
from yaml import safe_load
from aiogram import Bot, Dispatcher
from collections import defaultdict

with open ('config.yml') as c_stream:
    config = safe_load(c_stream)

# Объект бота
bot = Bot(token=config['bot_token'])
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
if config['log_level'] == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

MY_CHANNEL = config['tg_channel']

user_memory = {}
user_friends_memory = defaultdict(int)
post_memory = []

def clear_memory():
    user_memory.clear()
    user_friends_memory.clear()
    post_memory.clear()