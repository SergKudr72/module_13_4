from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = "7612810185:AAHYB9SIss78q2kU_j8I4D052Dsbmdhn0ko" #"token_bot???"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()    # добавил пол для расчета калорий

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

# добавил пол для расчета калорий
@dp.message_handler(state = UserState.weight)
async def fsm_set_gender(message, state):
    await state.update_data(first_weight = message.text)
    await message.answer('Введите свой пол (мужской или женский):')
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def fsm_send_calories(message, state):
    await state.update_data(first_gender = message.text)
    data = await state.get_data()
    if str(data['first_gender']) == "мужской":
        result_m = round(10*int(data['first_weight'])+6.25*int(data['first_growth'])-5*int(data['first_age'])+5, 2)
        await message.answer(f'Ваша норма калорий для мужчин: {result_m}')
        await state.finish()
    else:
        result_w = round(10*int(data['first_weight'])+6.25*int(data['first_growth'])-5*int(data['first_age'])-161, 2)
        await message.answer(f'Ваша норма калорий для женщин: {result_w}')
        await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
