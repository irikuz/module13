from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = " "
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ]
    ], resize_keyboard=True
)

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=inline_menu)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161")
    await call.answer()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = int(data["weight"])
    b = int(data["growth"])
    c = int(data["age"])
    norma = 10*a+6.25*b-5*c+-161
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=start_menu)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)