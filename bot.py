import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8985863047:AAEmsp6pXTkosCHkV-bJe64cRtB59lslAUU"
# Пользователи
SUPPORT_USERNAME = "estalememn"
SALES_USERNAME = "israelun"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

# Главное меню (кнопки внизу)
def get_main_kb():
    kb = [
        [KeyboardButton(text="🛒 Каталог товаров"), KeyboardButton(text="👤 Личный кабинет")],
        [KeyboardButton(text="💬 Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Инлайн-кнопка для связи с продавцом
def get_sales_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать продавцу", url=f"https://t.me/{SALES_USERNAME}")]
    ])
    return kb

# Инлайн-кнопка для связи с поддержкой
def get_support_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать в поддержку", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ])
    return kb

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Здравствуйте! Добро пожаловать в Npay Shop.**\n\n"
        "Мы предлагаем лучшие товары и качественный сервис.\n"
        "Выберите интересующий вас раздел в меню ниже:",
        reply_markup=get_main_kb(),
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(F.text == "🛒 Каталог товаров")
async def show_catalog(message: types.Message):
    await message.answer(
        "📦 **Каталог товаров Npay Shop**\n\n"
        "Выберите товар, который вас интересует, и нажмите кнопку ниже, чтобы оформить заказ.",
        reply_markup=get_sales_kb(),
        parse_mode=ParseMode.MARKDOWN
    )
    await message.answer("Напишите @israelun, что именно вы хотели бы приобрести.")

@dp.message(F.text == "👤 Личный кабинет")
async def show_profile(message: types.Message):
    user = message.from_user
    text = (
        f"👤 **Личный кабинет**\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"👤 Имя: {user.full_name}\n"
        f"Статус: Активен ✅"
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "💬 Поддержка")
async def show_support(message: types.Message):
    await message.answer(
        "🛠 **Служба поддержки Npay Shop**\n\n"
        "Напишите нашему специалисту свой вопрос, и мы ответим как можно скорее!",
        reply_markup=get_support_kb(),
        parse_mode=ParseMode.MARKDOWN
    )

# --- ЗАПУСК ---
async def main():
    print("Бот успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
