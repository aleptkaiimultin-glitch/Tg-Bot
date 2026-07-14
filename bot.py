import asyncio
import aiosqlite
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8985863047:AAEmsp6pXTkosCHkV-bJe64cRtB59lslAUU"
ADMIN_ID = 8814817662 
SUPPORT_USERNAME = "israelmemn"  # Поддержка
SALES_USERNAME = "israelun"      # Менеджер по продажам

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ (SQLite) ---
async def init_db():
    async with aiosqlite.connect("shop_data.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect("shop_data.db") as db:
        await db.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect("shop_data.db") as db:
        async with db.execute("SELECT id FROM users") as cursor:
            return [row[0] for row in await cursor.fetchall()]

# --- КЛАВИАТУРЫ ---
def get_main_kb():
    kb = [
        [KeyboardButton(text="🛒 Каталог товаров"), KeyboardButton(text="👤 Личный кабинет")],
        [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="🎁 Акции")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer(
        "👋 **Добро пожаловать в Npay Shop!**\n\n"
        "Лучший сервис для быстрых покупок. Выбери нужное действие в меню:",
        reply_markup=get_main_kb(),
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(F.text == "🛒 Каталог товаров")
async def show_catalog(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать менеджеру", url=f"https://t.me/{SALES_USERNAME}")]])
    await message.answer("📦 **Каталог Npay Shop**\nСвяжись с @israelun, чтобы оформить заказ.", reply_markup=kb)

@dp.message(F.text == "👤 Личный кабинет")
async def show_profile(message: types.Message):
    await message.answer(f"🆔 **Твой профиль**\n\nID: `{message.from_user.id}`\nСтатус: Покупатель Npay ✅")

@dp.message(F.text == "💬 Поддержка")
async def show_support(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")]])
    await message.answer("🛠 **Поддержка Npay Shop**\nНапиши специалисту @israelmemn, мы ответим как можно быстрее!", reply_markup=kb)

@dp.message(F.text == "🎁 Акции")
async def show_promo(message: types.Message):
    await message.answer("🔥 **Текущие акции:**\n\nСледи за новостями — скоро будут очень горячие предложения!")

# --- АДМИН-ПАНЕЛЬ ---
@dp.message(Command("admin"))
async def admin_menu(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        users = await get_all_users()
        await message.answer(f"👑 **Админ-панель**\nВсего юзеров в базе: {len(users)}\n\nКоманды:\n/broadcast [текст] — рассылка")

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/broadcast ", "")
        users = await get_all_users()
        count = 0
        for user_id in users:
            try:
                await bot.send_message(user_id, text)
                count += 1
            except: pass
        await message.answer(f"✅ Рассылка завершена. Успешно отправлено: {count}")

async def main():
    await init_db()
    print("Бот Npay Shop успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
