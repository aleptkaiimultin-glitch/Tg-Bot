import asyncio
import aiosqlite
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Настройки
TOKEN = "8985863047:AAEmsp6pXTkosCHkV-bJe64cRtB59lslAUU"
SUPPORT = "israelmemn"
SALES = "israelun"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация базы
async def init_db():
    async with aiosqlite.connect("shop.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect("shop.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
        await db.commit()

# Клавиатура
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог товаров"), KeyboardButton(text="Личный кабинет")],
    [KeyboardButton(text="Поддержка"), KeyboardButton(text="Акции")]
], resize_keyboard=True)

# Обработчики
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    await add_user(msg.from_user.id)
    await msg.answer("Добро пожаловать в Npay Shop.\nВыберите раздел в меню.", reply_markup=main_kb)

@dp.message(F.text == "Каталог товаров")
async def catalog(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать менеджеру", url=f"https://t.me/{SALES}")]])
    await msg.answer("Каталог товаров.\nДля заказа свяжитесь с @israelun.", reply_markup=kb)

@dp.message(F.text == "Личный кабинет")
async def profile(msg: types.Message):
    await msg.answer(f"ID: {msg.from_user.id}\nСтатус: Активен")

@dp.message(F.text == "Поддержка")
async def support(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать в поддержку", url=f"https://t.me/{SUPPORT}")]])
    await msg.answer("Техническая поддержка.\nСвяжитесь с @israelmemn.", reply_markup=kb)

@dp.message(Command("broadcast"))
async def broadcast(msg: types.Message):
    # Рассылка работает для всех, кто ввел команду
    command_args = msg.text.split(maxsplit=1)
    if len(command_args) > 1:
        text = command_args[1]
        async with aiosqlite.connect("shop.db") as db:
            async with db.execute("SELECT id FROM users") as cursor:
                users = await cursor.fetchall()
                for user in users:
                    try: await bot.send_message(user[0], text)
                    except: continue
        await msg.answer("Рассылка завершена.")

async def main():
    await init_db()
    print("Бот запущен. Ожидание сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
