from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import admin
from create_bot import bot


async def admin_menu(message: types.Message):
    if message.chat.type == "private":
        if message.from_user.id in admin:
            markup = InlineKeyboardMarkup(row_width=1)
            buttons = [
                InlineKeyboardButton("Статистика бота", callback_data="stat"),
                InlineKeyboardButton("Рассылка", callback_data="mailing"),
                InlineKeyboardButton("Выдать доступ к созданию заданий", callback_data="giving_create_menu")
            ]
            markup.add(*buttons)
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id,
                                   "Админ меню:",
                                   reply_markup=markup)




def reg(dp):
    dp.register_message_handler(admin_menu, commands='admin')