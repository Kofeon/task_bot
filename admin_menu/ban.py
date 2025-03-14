from create_bot import bot

from aiogram import types

from config import admin

# @dp.message_handler(lambda message: message.text.lower() == "анбан")
async def anban_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} разбанен.")
        except:
            pass

# @dp.message_handler(lambda message: message.text.lower() == "бан")
async def ban_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} забанен.\n"
                                f"Чтобы он снова мог зайти в группу, напишите анбан в ответ на его сообщение")
        except:
            pass


def reg(dp):
    dp.register_message_handler(anban_command, lambda message: message.text.lower() == "анбан")
    dp.register_message_handler(ban_command, lambda message: "бан" in message.text.lower())