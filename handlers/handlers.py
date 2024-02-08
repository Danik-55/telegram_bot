from aiogram import Router, types
from aiogram.filters import CommandStart, Command

private_router = Router()


@private_router.message(CommandStart())
async def starting_message(message: types.Message):
    await message.answer('Это приветственное сообщение')


@private_router.message(Command('second'))
async def starting_message(message: types.Message):
    await message.answer('Реакция на second message')


@private_router.message(Command('second'))
async def starting_message(message: types.Message):
    await message.answer('Реакция на second message')