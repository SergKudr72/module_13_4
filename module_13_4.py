from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = "token_bot???"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")

@dp.message_handler(text = ['Calories'])
async def set_age(message):
    await message.answer('Введите свой возраст (лет):')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def fsm_set_growth(message, state):
    await state.update_data(first_age = message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def fsm_set_weight(message, state):
    await state.update_data(first_growth = message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def fsm_send_calories(message, state):
    await state.update_data(first_weight = message.text)
    data = await state.get_data()
    result = round(10*int(data['first_weight']) + 6.25*int(data['first_growth']) - 5*int(data['first_age']) + 5, 2)
    await message.answer(f'Ваша норма калорий для мужчин: {result}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
