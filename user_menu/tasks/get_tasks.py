from database import cur, con
from create_bot import bot

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def all_telegram_channel_tasks(call: types.CallbackQuery):
    telegram_channel_tasks = cur.execute("SELECT * FROM telegram_channel_tasks").fetchall()
    markup = InlineKeyboardMarkup(row_width=1)
    for i in telegram_channel_tasks:
        task_id, channel, creator_id, type, quantity, executed_quantity, price, time, who_did = i
        if executed_quantity == quantity:
            cur.execute("DELETE FROM telegram_channel_tasks WHERE task_id = ?",
                        (task_id))
            con.commit()

        else:
            if str(call.from_user.id) not in who_did.split():
                button = InlineKeyboardButton(text=f"{type} {executed_quantity}/{quantity} {price} {time}", callback_data=f"{task_id}{type[0]}")
                markup.add(button)
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                            text="Все доступные задания:", reply_markup=markup)

def reg(dp):
    dp.register_callback_query_handler(all_telegram_channel_tasks, text="all_telegram_channel_tasks")