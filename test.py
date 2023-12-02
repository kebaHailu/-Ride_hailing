import asyncio 
from aiogram import types, Dispatcher , Bot 

TOKEN = '6689372696:AAHNYNiKiHymrQtmQ1lPu3wN_G9uFat3JcA'


dp = Dispatcher()


@dp.message_handler(commands=['start'])
async def start(msg:types.Message):
    await msg.answer('Hello, World!')


async def main():
    bot = Bot(TOKEN)

    await dp.start_polling(bot)



if __name__ == '__main__':
    
    asyncio.run(main())