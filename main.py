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
# class SignupFSM(StatesGroup):
#     username = State()
#     phone_number = State()
#     role = State()

# # for login 
# class LoginFSM(StatesGroup):
#     confirm_username = State()
#     confirm_password = State()

# # signup handler 
# @dp.message_handler(Command('signup'))
# async def signup_command(message: types.Message) -> None:
#     await message.answer('Please enter your username')
#     await SignupFSM.username.set() 
#     await message.answer('Please enter your phone')
#     await SignupFSM.phone.set()
#     await message.answer('Please enter your role')
#     await SignupFSM.role.set()

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
