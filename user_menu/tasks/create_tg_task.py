from database import cur, con
from create_bot import bot, redis

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                        ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class telegram_channel_tasks_state(StatesGroup):
    link = State()
    quantity = State()
    price = State()
    time = State()


async def create_task(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    button = [
        InlineKeyboardButton("Бусты", callback_data="b"),
        InlineKeyboardButton("Подписки", callback_data="s"),
        InlineKeyboardButton("Другой вид задания(ручная проверка)", callback_data="another")
    ]
    markup.add(*button)
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text="Выберите тип задания:",
                                reply_markup=markup)

async def requests(call: types.CallbackQuery):
    await redis.set("task_type", call.data)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton('Отмена')
    markup.add(cancel)

    await call.message.reply("Отправьте ссылку на канал", reply_markup=markup)
    await telegram_channel_tasks_state.link.set()


async def get_link(message: types.Message, state: FSMContext):
    text = message.text
    if "@" in text:
        text = text.replace("@", "https://t.me/")
    try:
        await state.update_data(channel=text)
        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer("Спасибо!\n\n"
                             "Теперь введите количество")
        await telegram_channel_tasks_state.next()
    except:
        await bot.delete_message(message.chat.id, message.message_id)

async def get_quantity(message: types.Message, state: FSMContext):
    try:
        await state.update_data(quantity=int(message.text))
        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer("Спасибо!\n\n"
                             "Теперь введите желаемую цену")
        await telegram_channel_tasks_state.next()
    except:
        await bot.delete_message(message.chat.id, message.message_id)

async def get_price(message: types.Message, state: FSMContext):
    # try:
    await state.update_data(price=float(message.text))
    await bot.delete_message(message.chat.id, message.message_id)

    data = await state.get_data()
    dollar_balance = int(
        cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (message.from_user.id,)).fetchone()[0])

    if data["quantity"] * float(message.text) <= dollar_balance:
        markup = InlineKeyboardMarkup()
        forever =  InlineKeyboardButton("Неограниченный срок", callback_data="forever")
        markup.add(forever)
        await message.answer("Спасибо!\n\n"
                             "Теперь введите количество дней, которое исполнители должны держать буст/подписку на вашем канале\n\n"
                             "Пример: 365",
                             reply_markup=markup)
        await telegram_channel_tasks_state.next()
    else:
        await message.answer("Простите, но ваш баланс меньше полученного произведения.\n"
                             "Пожалуйста, введите желаемую цену повторно, либо же отмените создание задания")
    # except:
    #     await bot.delete_message(message.chat.id, message.message_id)

async def get_forever_time(call: types.CallbackQuery, state: FSMContext):
    task_id = cur.execute("SELECT MAX(task_id) FROM telegram_channel_tasks").fetchone()[0]
    if task_id == None:
        task_id = 1
    # try:
    data = await state.get_data()

    task_type = await redis.get("task_type")

    cur.execute('INSERT INTO telegram_channel_tasks (task_id, channel, creator_id, type, quantity, executed_quantity, price, time, who_did) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (task_id+1, data['channel'], call.from_user.id, task_type, data['quantity'], 0, data['price'], "∞", ""))
    cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE id = ?',
                (data['quantity']*data['price'], call.from_user.id))
    con.commit()

    await bot.send_message(call.message.chat.id, "Спасибо! Ваше задание успешно создано!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

async def get_time(message: types.Message, state: FSMContext):
    task_id = cur.execute("SELECT MAX(task_id) FROM telegram_channel_tasks").fetchone()[0]
    if task_id == None:
        task_id = 1
    # try:
    data = await state.get_data()

    task_type = await redis.get("task_type")

    cur.execute('INSERT INTO telegram_channel_tasks (task_id, channel, creator_id, type, quantity, executed_quantity, price, time, who_did) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (task_id+1, data['channel'], message.from_user.id, task_type, data['quantity'], 0, data['price'], int(message.text), ""))
    cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE id = ?',
                (data['quantity']*data['price'], message.from_user.id))
    con.commit()

    await bot.delete_message(message.chat.id, message.message_id)

    await bot.send_message(message.chat.id, "Спасибо! Ваше задание успешно создано!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    # except:
    #     await bot.delete_message(message.chat.id, message.message_id)


async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Успешно отменено.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def reg(dp):
    dp.register_message_handler(cancel, lambda message: message.text == "Отмена", state="*")
    dp.register_callback_query_handler(create_task, text="create_telegram_channel_tasks")
    dp.register_callback_query_handler(requests, text=["boost", "subscribe"])
    dp.register_message_handler(get_link, state=telegram_channel_tasks_state.link)
    dp.register_message_handler(get_quantity, state=telegram_channel_tasks_state.quantity)
    dp.register_message_handler(get_price, state=telegram_channel_tasks_state.price)
    dp.register_callback_query_handler(get_forever_time, text="forever", state=telegram_channel_tasks_state.time)
    dp.register_message_handler(get_time, state=telegram_channel_tasks_state.time)