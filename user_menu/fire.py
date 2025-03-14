import random

import re

from database import cur, con

from create_bot import bot
from random import randint

from aiogram import types

# @dp.message_handler(lambda message: message.text.lower() in fire_words)
async def fire_command(msg: types.Message):
    balance = cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0]
    try:
        n = float(re.findall(r'-?\d+\.?\d*', msg.text)[0])
        if not n:
            n = int(re.findall(r'\d+', msg.text)[0])
        if n <= balance:
            if n >= 10:
                users = cur.execute("SELECT * FROM users").fetchall()
                users_index = []

                for i in range(10):
                    user = users[random.randint(0, len(users) - 1)][1]
                    users_index.append(f' <a href="https://t.me/{user}">{user}</a>')
                    cur.execute('UPDATE users SET dollar_balance = (dollar_balance + ?) WHERE name = ?',
                                (n / 10, user))
                    con.commit()

                cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE name = ?',
                            (n, msg.from_user.username))
                con.commit()

                users_index = ", ".join(users_index)
                await msg.answer(
                    f'<a href="https://t.me/{msg.from_user.username}">{msg.from_user.username}</a> раздал {n}$.\n\n'
                    f'{users_index} получили по {n / 10}$.', disable_web_page_preview=True)
            else:
                await bot.send_message(chat_id=msg.chat.id, text="Команда +fire имеет минимальное значение 10$")
                await bot.delete_message(message_id=msg.message_id, chat_id=msg.chat.id)
        else:
            await bot.send_message(chat_id=msg.chat.id, text="Недостаточный баланс")
            await bot.delete_message(message_id=msg.message_id, chat_id=msg.chat.id)
    except:
        pass
# <a href="https://example.com">Текст ссылки</a>
# tg://user?id=123456789

def reg(dp):
    dp.register_message_handler(fire_command, lambda message: "+fire" in message.text)