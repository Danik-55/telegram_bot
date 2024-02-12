import asyncio
from aiogram import Bot, Dispatcher, types
from handlers.handlers import private_router
from commands.cmnds import commands_list


import logging
import os
MUSIC_BOT_TOKEN = os.getenv('MUSIC_BOT_TOKEN')

bot = Bot(token=MUSIC_BOT_TOKEN)
ALLOWED_UPDATES = ['private']
dp = Dispatcher()
dp.include_router(private_router)


async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands_list, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())