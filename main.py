from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from config import TOKEN, OpenAI
from SQL.DataCardDay import CardDay
from SQL.DataUsers import Users
from SQL.HistoreCard import History, History_love
from SQL.DataAnswer import Questions, add_wisdoms, card_love
import os, random, asyncio, logging, openai, sqlite3, time

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
TOKEN = TOKEN
openai.api_key = OpenAI
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
hide_key_board = types.ReplyKeyboardRemove()
markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
markup0 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup0.row('Карта дня 🎴')
markup0.add('Вытянуть карту 🀄️', 'Расклад на отношения 🤍', 'Добавить мудрости 🤓', 'История гадания 📖')
markup0.row('Поговорить с Black magician 😈')
markup1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup1.add('Выйти!')
markup2 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup2.add('Вытянуть три карты')
markup3 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup3.add('Открыть карту прошлого')
markup4 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup4.add('Открыть карту нынешнего')
markup5 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup5.add('Открыть карту будущего')
inline_btn_1 = InlineKeyboardButton('Узнать больше', callback_data='read')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
inline_btn_10 = InlineKeyboardButton('Узнать больше', callback_data='card_day')
inline_kb10 = InlineKeyboardMarkup().add(inline_btn_10)
inline_btn_2 = InlineKeyboardButton('Узнать больше', callback_data='history')
inline_btn_9 = InlineKeyboardButton('Узнать больше', callback_data='read_love')
inline_kb9 = InlineKeyboardMarkup().add(inline_btn_9)
markup10 = types.ReplyKeyboardRemove()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.full_name}, меня зовут Black magician 😈\nЯ умею гадать, давай попробуем ?👇', reply_markup=markup0)
    data_users = Users(message.from_user.id, message.from_user.username, message.from_user.full_name)
    data_users.recorde_in_date()


@dp.message_handler(commands=['info'])
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Black magician, целитель магии и разума\n\n🌌Дитя вселенной\n♑️Козерог 12:32  21.11.2022\n\nЯ здесь, чтобы сообщить моему сообществу, когда что-то идет не так, а затем направить омоложение, чтобы снова сделать все правильно.')


class do(StatesGroup):
    add_wisdom = State()
    speaking = State()


@dp.message_handler(content_types=['text'], state=None)
async def main(message: types.Message):
    print(message.from_user.id, message.from_user.full_name, message.text)
    global name
    name = random.choice(os.listdir("parser/static/img")).split('.jpg')[0]
    if message.text == 'Карта дня 🎴':
        con = sqlite3.connect('BlackBot.db')
        cur = con.cursor()
        time = cur.execute(f'SELECT full_time FROM card_day WHERE user_id = {message.from_user.id}').fetchall()
        global name_card
        name_card = cur.execute(f'SELECT name_card FROM card_day WHERE user_id = {message.from_user.id}').fetchall()
        def isUserDatebase():
            data = cur.execute('SELECT * FROM card_day')
            for i in data.fetchall():
                if message.from_user.id == i[0]:
                    return True
            return False
        if not isUserDatebase():
            current_datetime = datetime.now()
            await bot.send_message(message.from_user.id, '🔮')
            await asyncio.sleep(3)
            await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
            with open(f'parser/static/txt/{name}.txt', 'r', encoding='utf8') as read:
                info = read.read()
                await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb1)
                card = CardDay(message.from_user.id, name, current_datetime.day)
                card.recorde_in_date()
        else:
            current_datetime = datetime.now()
            if current_datetime.day - int(time[0][0]) == 1:
                current_datetime = datetime.now()
                await bot.send_message(message.from_user.id, '🔮')
                await asyncio.sleep(3)
                await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
                with open(f'parser/static/txt/{name}.txt', 'r', encoding='utf8') as read:
                    info = read.read()
                    await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb1)
                    card = CardDay(message.from_user.id, name, current_datetime.day)
                    card.recorde_in_date()
            else:
                await bot.send_message(message.from_user.id, '🔮')
                await asyncio.sleep(3)
                await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name_card[0][0]}.jpg', 'rb'))
                with open(f'parser/static/txt/{name_card[0][0]}.txt', 'r', encoding='utf8') as read:
                    info = read.read()
                    await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb10)
    elif message.text == 'Вытянуть карту 🀄️':
        await bot.send_message(message.from_user.id, '🔮')
        await asyncio.sleep(3)
        await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
        with open(f'parser/static/txt/{name}.txt', 'r', encoding='utf8') as read:
            info = read.read()
            await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb1)
            data_questions = Questions(message.from_user.id, message.from_user.full_name, info, name)
            data_questions.recorde_in_data()
    elif message.text == 'История гадания 📖':
        his = History(message.from_user.id)
        his_love = History_love(message.from_user.id)
        if not his.isUserDatebase() and not his_love.isUserDatebase():
            await bot.send_message(message.from_user.id, 'Вы еще не гадали 👿')
        elif not his_love.isUserDatebase():
            for i in range(1, 5):
                await bot.send_message(message.from_user.id, f'Категория: Карта дня 🀄️{his.read_card()[i-1][0][:200]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Узнать больше', callback_data=f'history{i}')))
        elif not his.isUserDatebase():
            for i in range(1, 5):
                await bot.send_message(message.from_user.id, f'Категория: Расклад на отношения 🤍️{his_love.read_card_love()[i-1][0][:200]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Узнать больше', callback_data=f'history_love{i}')))
        else:
            for i in range(1, 5):
                await bot.send_message(message.from_user.id, f'Категория: Карта дня 🀄️{his.read_card()[i - 1][0][:200]}', reply_markup=InlineKeyboardMarkup().add( InlineKeyboardButton('Узнать больше', callback_data=f'history{i}')))
                await bot.send_message(message.from_user.id, f'Категория: Расклад на отношения 🤍️{his_love.read_card_love()[i - 1][0][:200]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Узнать больше', callback_data=f'history_love{i}')))
    elif message.text == 'Добавить мудрости 🤓':
        await do.add_wisdom.set()
        await bot.send_message(message.from_user.id, 'Оставь свой отзыв, скажи что нам добавить или улучшить ✨', reply_markup=markup1)
    elif message.text == 'Расклад на отношения 🤍':
        await bot.send_message(message.from_user.id, 'Этот расклад даст общее понимание о сложившейся ситуации по вашему вопросу.', reply_markup=markup2)
    elif message.text == 'Вытянуть три карты':
        await bot.send_photo(message.from_user.id, photo=open('parser/static/taro 3 card.jpg', 'rb'))
        await bot.send_message(message.from_user.id, 'Открыть карты 👇', reply_markup=markup3)
    elif message.text == 'Открыть карту прошлого':
        await bot.send_message(message.from_user.id, '🔮')
        await asyncio.sleep(3)
        await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
        with open(f'parser/static/txt_love/{name}.txt', 'r', encoding='utf8') as read:
            info = read.read()
            await bot.send_message(message.from_user.id, '<b>Карта прошлого</b>', reply_markup=markup4)
            await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb9)
            data_love = card_love(message.from_user.id, message.from_user.full_name, name, info)
            data_love.write()
    elif message.text == 'Открыть карту нынешнего':
        await bot.send_message(message.from_user.id, '🔮')
        await asyncio.sleep(3)
        await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
        with open(f'parser/static/txt_love/{name}.txt', 'r', encoding='utf8') as read:
            info = read.read()
            await bot.send_message(message.from_user.id, '<b>Карта нынешнего</b>', reply_markup=markup5)
            await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb9)
            data_love = card_love(message.from_user.id, message.from_user.full_name, name, info)
            data_love.write()
    elif message.text == 'Открыть карту будущего':
        await bot.send_message(message.from_user.id, '🔮')
        await asyncio.sleep(3)
        await bot.send_photo(message.from_user.id, photo=open(f'parser/static/img/{name}.jpg', 'rb'))
        with open(f'parser/static/txt_love/{name}.txt', 'r', encoding='utf8') as read:
            info = read.read()
            await bot.send_message(message.from_user.id, '<b>Карта будущего</b>')
            await bot.send_message(message.from_user.id, info[:200], reply_markup=inline_kb9)
            await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup0)
            data_love = card_love(message.from_user.id, message.from_user.full_name, name, info)
            data_love.write()
    elif message.text == 'Поговорить с Black magician 😈':
        await do.speaking.set()
        await bot.send_message(message.from_user.id, 'Начни вести диалог!\n(если хотите выйти нажмите на кнопку внизу!)', reply_markup=markup1)
    else:
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup0)


@dp.callback_query_handler(text='card_day')
async def read_more(callback: types.CallbackQuery):
    with open(f'parser/static/txt/{name_card[0][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.message_handler(state=do.speaking)
async def add_wisdom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['speaking'] = message.text
    if data['speaking'] == 'Выйти!':
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup0)
        await state.finish()
    else:
        conversation = ''
        questions = data['speaking']
        conversation += '\nЧеловек: ' + questions + '\nИИ:'
        response = openai.Completion.create(
            engine='davinci',
            prompt=conversation,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=['\n', 'Человек:', 'ИИ:']
        )
        anwer = response.choices[0].text.strip()
        conversation += anwer
        await message.reply(anwer, reply_markup=markup1)
        await do.speaking.set()


@dp.message_handler(state=do.add_wisdom)
async def add_wisdom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['add_wisdom'] = message.text
    if data['add_wisdom'] == 'Выйти!':
        await state.finish()
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup0)
    else:
        await bot.send_message(message.from_user.id, 'Спасибо за вашу мудрость!\nЯ прислушаюсь к вам.')
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markup0)
        await state.finish()
        wisdoms = add_wisdoms(message.from_user.id, message.from_user.full_name, data['add_wisdom'])
        wisdoms.write_wisdoms()


@dp.callback_query_handler(text='read')
async def read_more(callback: types.CallbackQuery):
    with open(f'parser/static/txt/{name}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='read_love')
async def read_more(callback: types.CallbackQuery):
    with open(f'parser/static/txt_love/{name}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history1')
async def read_more_history(callback: types.CallbackQuery):
    his = History(callback.from_user.id)
    with open(f'parser/static/txt/{his.read_name_card()[0][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history2')
async def read_more_history(callback: types.CallbackQuery):
    his = History(callback.from_user.id)
    with open(f'parser/static/txt/{his.read_name_card()[1][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history3')
async def read_more_history(callback: types.CallbackQuery):
    his = History(callback.from_user.id)
    with open(f'parser/static/txt/{his.read_name_card()[2][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history4')
async def read_more_history(callback: types.CallbackQuery):
    his = History(callback.from_user.id)
    with open(f'parser/static/txt/{his.read_name_card()[3][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history5')
async def read_more_history(callback: types.CallbackQuery):
    his = History(callback.from_user.id)
    with open(f'parser/static/txt/{his.read_name_card()[4][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history_love1')
async def read_more_history(callback: types.CallbackQuery):
    his_love = History_love(callback.from_user.id)
    with open(f'parser/static/txt_love/{his_love.read_name_card_love()[0][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history_love2')
async def read_more_history(callback: types.CallbackQuery):
    his_love = History_love(callback.from_user.id)
    with open(f'parser/static/txt_love/{his_love.read_name_card_love()[1][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history_love3')
async def read_more_history(callback: types.CallbackQuery):
    his_love = History_love(callback.from_user.id)
    with open(f'parser/static/txt_love/{his_love.read_name_card_love()[2][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history_love4')
async def read_more_history(callback: types.CallbackQuery):
    his_love = History_love(callback.from_user.id)
    with open(f'parser/static/txt_love/{his_love.read_name_card_love()[3][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


@dp.callback_query_handler(text='history_love5')
async def read_more_history(callback: types.CallbackQuery):
    his_love = History_love(callback.from_user.id)
    with open(f'parser/static/txt_love/{his_love.read_name_card_love()[5][0]}.txt', 'r', encoding='utf8') as read:
        info = read.read()
        if len(info) > 4096:
            await callback.message.edit_text(info[:4096])
            await bot.send_message(callback.from_user.id, info[4096:8192])
        else:
            await callback.message.edit_text(info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
else:
    print('Бот не работает!')
