from aiogram import types
from config import admin
from database import cur, con
import re

# @dp.message_handler(lambda message: "-xp" in message.text.lower())
async def minus_xp_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            dollar_balance = float(re.findall(r'-?\d+\.?\d*', message.text)[0])
            if not dollar_balance:
                dollar_balance = int(re.findall(r'\d+', message.text)[0])
            cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE id = ?',
                        (dollar_balance, message.reply_to_message.from_user.id))
            con.commit()
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} -{dollar_balance}$")
        except:
            pass


def reg(dp):
    dp.register_message_handler(minus_xp_command, lambda message: "-dl" in message.text.lower())