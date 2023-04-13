from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from datetime import datetime
from random import choice
import json
import os
import asyncio

BOT_TOKEN: str = '1541721067:AAH7YRcfoG_YIDH8li2NTrI7TtR_y5TS-FM'
# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


def rule(w):
    w = str(w)
    for k in range(len(w)):
        if w[-k - 1] in first_letters:
            return w[-k - 1]


with open("cities_rus.json", "r") as f:
    cities = json.load(f)
first_letters = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'ы', 'э', 'ю', 'я']

dlina = 0
for i in cities:
    dlina += len(cities.get(i))

global bot_word

book = {}
# /start
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'\n\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")},'
                f' id {message.from_user.id}, @{message.from_user.username}, '
                f'{message.from_user.first_name} {message.from_user.last_name}, {message.from_user.language_code}\n')

    global bot_word
    book[message.from_user.id] = []
    await message.answer('Привет!\nДавай сыграем в города.\n'
                         f'Я знаю городов: {dlina}.\n\nМожешь отправить:\n/start для рестарта\n'
                         f'/add для добавления городов\n/help для чтения правил'
                         f'\n/stop для завершения игры и просмотра итога.')
    r = choice(first_letters)
    bot_word = choice(cities[r])
    book[message.from_user.id].append(bot_word)
    await message.answer(f'Я начну: {bot_word}')
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'{bot_word.upper()} ')


# конец игры
@dp.message(Command(commands=['stop']))
async def process_cancel_command(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write('/stop ')
    if book.get(message.from_user.id):
        end = ''
        for j in book[message.from_user.id]:
            end += (j + ', ')
        await message.answer(f'Конец, мы назвали {len(book[message.from_user.id])} города(ов): {end[:-2]}.')
        book[message.from_user.id].clear()
    else:
        await message.answer('Так мы еще не начали, жми /start')


# help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write('/help ')
    if book.get(message.from_user.id):
        await message.answer(f'Отправь мне город, начинающийся на последнюю букву моего города. Если это Ь или Ъ - то '
                             f'бери следующую с конца букву.\n'
                             f'А на букву Ы, если что, я знаю {len(cities["ы"])} городов.'
                             f'\n\nСейчас тебе на {rule(bot_word).upper()}!')
    else:
        await message.answer(f'Отправь мне город, начинающийся на последнюю букву моего города. Если это Ь или Ъ - то '
                             f'бери следующую с конца букву.\n'
                             f'А на букву Ы, если что, я знаю {len(cities["ы"])} городов.')


# добаление городов
@dp.message(Command(commands=['add']))
async def add(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write('/add ')
    await message.answer('Функция пока не работает :(')
    # await message.answer('Вводи города одним сообщением через пробел, чтобы добавить их в мою базу')
    # async with asyncio.wait_for(message.text, timeout=) as new_message:
    #     adds = str(message.text).split()
    #     with open("add.txt", "a", encoding='utf-8') as w:
    #         w.write(*adds)
    #         w.write('\n\n')
    #     await message.answer(f'Внесено городов на рассмотрение моим хозяином: {len(adds)}.')


# если ввод не на доступную букву
@dp.message(lambda x: x.text and rule(x) not in first_letters)
async def process_text_answer(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'{str(message.text)} ')
    await message.answer(f'Я могу только по-русски, тебе на {rule(bot_word).upper()}')


# остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    global bot_word
    player_word = str(message.text)
    adds = str(message.text)
    with open("add.txt", "a", encoding='utf-8') as w:
        # w.write(f'{str(message.from_user.id), str(message.from_user.first_name), str(message.from_user.last_name)}')
        w.write(f'{adds.capitalize()} ')

    if player_word[0].lower() == rule(bot_word).lower():
        if player_word.upper() in book[message.from_user.id] or player_word.capitalize() in book[message.from_user.id]:
            await message.answer('Этот город уже был!')
        elif player_word.capitalize() in cities[player_word.lower()[0]]:
            book[message.from_user.id].append(player_word.capitalize())
            while bot_word in book[message.from_user.id] or bot_word[0].lower() != rule(player_word).lower():
                bot_word = choice(cities[rule(player_word)])
            await message.answer(bot_word)
            with open("add.txt", "a", encoding='utf-8') as w:
                w.write(f'{bot_word.upper()} ')
            player_word = ''
            book[message.from_user.id].append(bot_word)
        else:
            await message.answer(f'Не знаю такого, попробуй еще - тебе на {rule(bot_word).upper()}')
    else:
        await message.answer(f'Первая буква не подходит, тебе на {rule(bot_word).upper()}')
    print(book)


if __name__ == '__main__':
    dp.run_polling(bot)
