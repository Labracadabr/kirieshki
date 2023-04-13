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


book = {}
mode = ''
# /start
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    global user
    user = message.from_user.id
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'\n\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")},'
                f' id {user}, @{message.from_user.username}, '
                f'{message.from_user.first_name} {message.from_user.last_name}, {message.from_user.language_code}\n')

    book[user] = {"used": [], "bot_word": '', "player_word": '', mode: 'Hard'}
    await message.answer('Привет!\nДавай сыграем в города.\n'
                         f'Я знаю городов: {dlina}.\n\nМожешь отправить:\n/start для рестарта\n'
                         f'/mode для смены сложности\n'
                         f'/add для добавления городов\n/help для чтения правил'
                         f'\n/stop для завершения игры и просмотра итога.')
    r = choice(first_letters)
    book[user]["bot_word"] = choice(cities[r])
    book[user]["used"].append(book[user]["bot_word"])
    await message.answer(f'Я начну: {book[user]["bot_word"]}')
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'{book[user]["bot_word"].upper()} ')

# gamemode
@dp.message(Command(commands=['mode']))
async def process_cancel_command(message: Message):
    user = message.from_user.id
    if book.get(user):
        if book[user][mode] == 'Hard':
            book[user][mode] = 'Easy'
        else:
            book[user][mode] = 'Hard'
        await message.answer(f'Режим изменен на {book[user][mode]}. Тебе на {rule(book[user]["bot_word"]).upper()}.')
    else:
        await message.answer('Режим можно изменить только во время игры - /start.\n'
                             'При старте режим автоматически станет Hard.')


# конец игры
@dp.message(Command(commands=['stop']))
async def process_cancel_command(message: Message):
    user = message.from_user.id
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write('/stop ')
    if book.get(user):
        end = ''
        for j in book[user]['used']:
            end += (j + ', ')
        await message.answer(f'Конец, мы назвали {len(book[user]["used"])} города(ов): {end[:-2]}.')
        book[user].clear()
    else:
        await message.answer('Так мы еще не начали, жми /start')


# help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    user = message.from_user.id
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write('/help ')
    if book.get(user):
        await message.answer(f'Отправь мне город, начинающийся на последнюю букву моего города.\n\n'
                             f'Если это Ь или Ъ - то бери следующую с конца букву, например:\n'
                             f'Если я пишу "Казань" - ты можешь написать "Найроби"\n\n'
                             f'Есть два режима игры:\nHard - я принимаю от тебя только те города, '
                             f'которые сам знаю;\nEasy - я не проверяю, знаю ли город из твоего ответа.\n'
                             f'Нажми /mode для смены режима.\n\n'
                             f'А на букву Ы, если что, я знаю {len(cities["ы"])} городов.'
                             f'\n\nСейчас тебе на {rule(book[user]["bot_word"]).upper()}!')
    else:
        await message.answer(f'Отправь мне город, начинающийся на последнюю букву моего города.\n\n'
                             f'Если это Ь или Ъ - то бери следующую с конца букву, например:\n'
                             f'Если я пишу "Анадырь" - ты можешь написать "Рим"\n\n'
                             f'Есть два режима игры:\nHard - я принимаю от тебя только те города, '
                             f'которые сам знаю;\nEasy - я не проверяю, знаю ли город из твоего ответа.\n'
                             f'Нажми /mode для смены режима.\n\n'
                             f'А на букву Ы, если что, я знаю {len(cities["ы"])} городов.\n\n'
                             f'Для начала игры нажми /start')


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
@dp.message(lambda x: x.text and str(x.text).lower()[-1] not in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
async def process_text_answer(message: Message):
    with open("add.txt", "a", encoding='utf-8') as w:
        w.write(f'{str(message.text)} ')
    await message.answer(f'Я могу только по-русски, тебе на {rule(book[user]["bot_word"]).upper()}')
    print(str(message.text).lower()[-1])


# остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    book[user]["player_word"] = str(message.text)
    adds = str(message.text)
    with open("add.txt", "a", encoding='utf-8') as w:
        # w.write(f'{str(user), str(message.from_user.first_name), str(message.from_user.last_name)}')
        w.write(f'{adds.capitalize()} ')

    # checks if player_word is ok
    if book[user]["player_word"][0].lower() == rule(book[user]["bot_word"]).lower():
        if book[user]["player_word"].capitalize() in book[user]["used"]: # or book[user]["player_word"].capitalize() in book[user]:
            await message.answer('Этот город уже был!')
        elif book[message.from_user.id][mode] == 'Easy' or book[user]["player_word"].capitalize() in cities[book[user]["player_word"].lower()[0]]:
            book[user]["used"].append(book[user]["player_word"].capitalize())

            # generate bot response
            while book[user]["bot_word"] in book[user]["used"] or book[user]["bot_word"][0].lower() != rule(book[user]["player_word"]).lower():
                book[user]["bot_word"] = choice(cities[rule(book[user]["player_word"])])
            await message.answer(book[user]["bot_word"])
            with open("add.txt", "a", encoding='utf-8') as w:
                w.write(f'{book[user]["bot_word"].upper()} ')
            book[user]["player_word"] = ''
            book[user]["used"].append(book[user]["bot_word"])

        else:
            await message.answer(f'Не знаю такого, попробуй еще - тебе на {rule(book[user]["bot_word"]).upper()}')
    else:
        await message.answer(f'Первая буква не подходит, тебе на {rule(book[user]["bot_word"]).upper()}')
    print(user, book[user]["used"])


if __name__ == '__main__':
    dp.run_polling(bot)
