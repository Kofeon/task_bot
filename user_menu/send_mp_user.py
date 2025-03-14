from aiogram import types
from database import cur, con
from create_bot import bot

from config import admin
import re


# @dp.message_handler(lambda message: "+xp" in message.text.lower())
async def plus_xp_command(message: types.Message):
    if message.from_user.id in admin:
        try:
            plus_mp = float(re.findall(r'-?\d+\.?\d*', message.text)[0])
            if not plus_mp:
                plus_mp = int(re.findall(r'\d+', message.text)[0])
            cur.execute('UPDATE users SET dollar_balance = (dollar_balance + ?) WHERE id = ?',
                        (plus_mp, message.reply_to_message.from_user.id))
            con.commit()
            await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} +{plus_mp}$")
        except:
            pass
    else:
        try:
            send_mp = float(re.findall(r'-?\d+\.?\d*', message.text)[0])
            if not send_mp:
                send_mp = int(re.findall(r'\d+', message.text)[0])

            balance = cur.execute("SELECT dollar_balance from users WHERE id = ?", (message.from_user.id,)).fetchone()[0]
            if balance >= send_mp:
                cur.execute('UPDATE users SET dollar_balance = (dollar_balance + ?) WHERE id = ?',
                            (send_mp, message.reply_to_message.from_user.id))
                con.commit()
                cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE id = ?',
                            (send_mp, message.from_user.id))
                con.commit()
                await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} +{send_mp}$\n"
                                    f"Пользователь {message.from_user.full_name} -{send_mp}$")
            else:
                await message.answer("Ваш баланс меньше заявленной суммы")
                await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        except:
            pass


def reg(dp):
    dp.register_message_handler(plus_xp_command, lambda message: "+send" in message.text.lower() or "+dl" in message.text.lower())