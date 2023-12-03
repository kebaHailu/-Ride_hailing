import asyncio , os
from imaplib import Commands
from aiogram import types, Dispatcher, Bot
from telegram import ReplyKeyboardRemove 
from hide import TOKEN_API, MONGODB_URL
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State , StatesGroup
from aiogram.filters.callback_data import CallbackData 
from aiogram.utils.markdown import hbold

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dp = Dispatcher()

# connecting with mongo server 
mongodb_url = MONGODB_URL
client = MongoClient(mongodb_url, server_api=ServerApi('1'))

db = client['BotDB']
users_collection = db['users']


class SignupFSM(StatesGroup):
    username = State()
    phone_number = State()
    role = State()

# for signup
@dp.message(Command('SignUp'))
async def signup_command(message:Message, state:FSMContext) -> None:
    await state.set_state(SignupFSM.username)
    await message.answer(
        "Welcome to the signup process!\n Please enter your username:",
        reply_markup=ReplyKeyboardRemove(),
        )

@dp.message(SignupFSM.username)
async def process_username(message: types.Message, state: FSMContext) -> None:
    username = message.text.strip() 
    if not username:
        await message.answer("Please enter a valid username")
        return
    
    if users_collection.find_one({'username': username}):
        await message.answer("This username is already taken")
        return
    
    await state.update_data(username=username)
    await message.answer("Please enter your phone number:")
    await SignupFSM.next()

# @dp.message(types.ContentType.CONTACT, SignupFSM.phone_number)
# async def process_phone_number(message: types.Message, state: FSMContext) -> None:
#     phone_number = message.contact.phone_number 
#     if not phone_number:
#         await message.answer("Please Share your phone number")
#         return 
#     await state.update_data(phone_number=phone_number)
#     markup = types.InlineKeyboardMarkup() 
#     driver_button = types.InlineKeyboardButton("Driver", callback_data='Driver')
#     passenger_button = types.InlineKeyboardButton("Passenger", callback_data="passenger")
#     markup.add(driver_button,row_width=1)
#     markup.add(passenger_button) 
#     await message.answer("Please Choose your role: ", reply_markup=markup)
#     await SignupFSM.next()
     





# # login handler
# @dp.message_handler()
# async def login_command(message: types.Message) -> None:
#     await message.answer('Please enter your username')
#     await LoginFSM.confirm_username.set()
#     await message.answer('Please enter your password')
#     await LoginFSM.confirm_password.set()

# # signup handler


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message):
    # reply_txt = f'Hello, {hbold(msg.from_user.full_name)}'
    await msg.answer("hello how are you ?")


async def main() -> None:

    token = TOKEN_API
    bot = Bot(token, parse_mode='HTML')
    await dp.start_polling(bot)


    


if __name__ == "__main__":
    asyncio.run(main()) 
