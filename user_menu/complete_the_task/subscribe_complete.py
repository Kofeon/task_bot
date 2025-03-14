from database import cur, con
from create_bot import bot, redis

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def subscribe_task(call: types.CallbackQuery):
    type = cur.execute("SELECT type FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    channel = cur.execute("SELECT channel FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    quantity = cur.execute("SELECT quantity FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    executed_quantity = cur.execute("SELECT executed_quantity FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    price = cur.execute("SELECT price FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    time = cur.execute("SELECT time FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]

    await redis.set("task_id", task_id)
    await redis.set("channel", channel)

    markup = InlineKeyboardMarkup(row_width=1)
    link = InlineKeyboardButton("Ссылка", url=channel)
    confirm = InlineKeyboardButton("Подтвердить выполнение задания", callback_data="confirm")
    markup.add(link, confirm)

    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text=f"Тип: {type}\n"
                                     f"Доступно: {quantity-executed_quantity}/{quantity}\n"
                                     f"Цена за выполнение: {price}$\n"
                                     f"Время, до которого нужно держать задание: {time}\n\n"
                                     f"Чтобы выполнить задание перейдите по ссылке,"
                                     f"а затем потвердите подписку.", reply_markup=markup
                                )

async def confirm_subscription(call: types.CallbackQuery):
    # user_channel_status = await bot.get_chat_member(chat_id='@chatid', user_id=call.from_user.id)
    # if user_channel_status["status"] != 'left':
    #     pass
    # else:
    #     await bot.send_message(call.from_user.id, 'text if not in group')
    markup = InlineKeyboardMarkup()
    mm = InlineKeyboardButton("Главное меню", callback_data="main_menu")
    markup.add(mm)

    task_id = await redis.get("task_id")
    task_id = task_id.decode("utf-8")
    price = await redis.get("price")
    price = price.decode("utf-8")

    cur.execute(
        'UPDATE telegram_channel_tasks SET executed_quantity = (executed_quantity + ?), who_did = (who_did || ?) WHERE task_id = ?',
        (1, f" {call.from_user.id}", task_id))
    cur.execute("UPDATE users SET dollar_balance = (dollar_balance + ?) WHERE id = ?",
                (price, call.from_user.id))
    con.commit()

    await bot.edit_message_text("Задание успешно выполнено\n"
                                f"Вы получили {price}$",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=markup)
    # time = cur.execute("SELECT time FROM telegram_channel_tasks WHERE task_id = ?", (task_id,)).fetchone()[0]
    # now = ""
    # while now != time:
    #     now = datetime.now().date()
    # await bot.send_message(call.message.chat.id, f'Время вышло!\n\n'
    #                                              f'Вы можете отписаться от <a href="{channel}">канала</a>')


subscribe_ids = []
telegram_channel_tasks = cur.execute("SELECT * FROM telegram_channel_tasks").fetchall()
for i in telegram_channel_tasks:
    task_id, channel, creator_id, type, quantity, executed_quantity, price, time, who_did = i
    if type[0] == "s":
        subscribe_ids.append(f"{task_id}s")

def reg(dp):
    dp.register_callback_query_handler(subscribe_task, text=subscribe_ids)
    dp.register_callback_query_handler(confirm_subscription, text="confirm")