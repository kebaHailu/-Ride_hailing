import asyncio , os
from imaplib import Commands
from aiogram import types, Dispatcher, Bot 
from dotenv import load_dotenv

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State , StatesGroup
from aiogram.filters.callback_data import CallbackData 
from aiogram.utils.markdown import hbold 
from pymongo import MongoClient

dp = Dispatcher()

# connecting with mongo server 

mongodb_url = os.getenv('MONGODB_URL')

client = MongoClient(mongodb_url)
db = client['BotDB']
users_collection = db['users']

# for signup 
class SignupFSM(StatesGroup):
    username = State()
    phone_number = State()
    role = State()

# # for login 
# class LoginFSM(StatesGroup):
#     confirm_username = State()
#     confirm_password = State()

# # signup handler 
@dp.message(Command('signup'))
async def signup_command(message: types.Message) -> None:
    await message.answer("Welcome to the signup process!\n Please enter your username:")
    await SignupFSM.username.set() 

@dp.message(state=SignupFSM.username)
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

@dp.message(content_types=types.ContentType.CONTACT, state=SignupFSM.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number 
    if not phone_number:
        await message.answer("Please Share your phone number")
        return 
    await state.update_data(phone_number=phone_number)
    markup = types.InlineKeyboardMarkup() 
    driver_button = types.InlineKeyboardButton("Driver", callback_data='Driver')
    passenger_button = types.InlineKeyboardButton("Passenger", callback_data="passenger")
    markup.add(driver_button,row_width=1)
    markup.add(passenger_button) 
    await message.answer("Please Choose your role: ", reply_markup=markup)
    await SignupFSM.next()
     





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
    load_dotenv('.env')
    token = os.getenv('TOKEN_API')
    
    bot = Bot(token, parse_mode='HTML')
    await dp.start_polling(bot)


    


if __name__ == "__main__":
    asyncio.run(main()) 
