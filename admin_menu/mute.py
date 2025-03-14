from create_bot import bot

from aiogram.types import ChatPermissions
from aiogram import types

from config import admin

# @dp.message_handler(lambda message: message.text.lower() == "анмут")
async def anmute_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=ChatPermissions(can_send_messages=True)
            )
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} успешно размучен")
        except:
            pass

# @dp.message_handler(lambda message: message.text.lower() == "мут")
async def mute_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} лишен права говорить.\n"
                                f"Чтобы он снова мог писать, напишите анмут в ответ его сообщения")
        except:
            pass

def reg(dp):
    dp.register_message_handler(anmute_command, lambda message: "анмут" in message.text.lower())
    dp.register_message_handler(mute_command, lambda message: "мут" in message.text.lower())