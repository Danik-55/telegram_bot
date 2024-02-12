import random

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
import requests


from os import getenv
from users.users import user

private_router = Router()
MUSIC_BOT_TOKEN = getenv('MUSIC_BOT_TOKEN')


@private_router.message(CommandStart())
async def starting_message(message: types.Message):
    await message.answer('Это приветственное сообщение')


@private_router.message(Command('second'))
async def starting_message(message: types.Message):
    await message.answer('Реакция на second message')


@private_router.message(F.text.lower() == 'игра')
async def random_game(message: types.Message):
    await message.answer('Игра угадайка. Правила игры - /rules. Хотите сыграть?')


@private_router.message(Command('rules'))
async def game_rules(message: types.Message):
    await message.answer('Правила игра таковы\nБот загадывает число от 1 до 100\n\
У вас есть 5 попыток чтобы угадать число, сыграем?')


@private_router.message(F.text.lower().in_(['да', 'давай', 'хочу', 'сыграем', 'хочу играть']))
async def positive_answer(message: types.Message):
    if not user['in_game']:
        random_number = random.randint(1, 100)
        user['in_game'] = True
        user['secret_number'] = random_number
        user['attempts'] = 5
    await message.answer('Бот загадал число! Игра началась!')


@private_router.message(F.text.lower().in_(['нет', 'не хочу', 'не буду', 'не хочу играть']))
async def negative_answer(message: types.Message):
    if not user['in_game']:
        await message.answer('Мы с вами не играем. Если захотите сыграть - пишите команду "игра"')
    else:
        await message.answer('Если хотите выйти из игры - напишите комманду /cancel в чат')


@private_router.message(Command('cancel'))
async def cancelling_game(message: types.Message):
    if user['in_game']:
        await message.answer('Отменяю игру')
        user['in_game'] = False
        await message.answer('Игра отменена')
    else:
        await message.answer('Игра не запущена, чтобы ее можно было отменить')


@private_router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def guessing_number(message: types.Message):
    if user['in_game']:
        if user['attempts'] > 0:
            if int(message.text) == user['secret_number']:
                await message.answer('Поздравляем! Вы выиграли! Хотите сыграть еще?')

            elif int(message.text) > user['secret_number']:
                await message.answer('Загаданное число меньше')
                user['attempts'] -= 1

            elif int(message.text) < user['secret_number']:
                await message.answer('Загаданное число больше')
                user['attempts'] -= 1

        if user['attempts'] == 0:
            await message.answer(f'У вас закончились попытки, загаданное число было\
{user["secret_number"]}\nХотите сыграть еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Чтобы я реагировал на числа - мы должны играть в игру!\nВведите комманду "игра"')


@private_router.message((F.text.lower() == 'кот') | (F.text.lower().contains('кот')))
async def cat_api(message: types.Message):
    API_URL = 'https://api.telegram.org/bot'
    API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
    ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('

    cat_response: requests.Response
    cat_link: str
    personal_id = message.from_user.id

    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        requests.get(f'{API_URL}{MUSIC_BOT_TOKEN}/sendPhoto?chat_id={personal_id}&photo={cat_link}')
    else:
        requests.get(f'{API_URL}{MUSIC_BOT_TOKEN}/sendMessage?chat_id={personal_id}&text={ERROR_TEXT}')


@private_router.message(F.voice)
async def check_message(message: types.Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    await message.answer('Это было голосовое сообщение')
