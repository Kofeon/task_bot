from database import cur, con
from create_bot import bot, redis

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                        ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class another_tasks_state(StatesGroup):
    text = State()
    quantity = State()
    price = State()


async def create_task(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Скриншот/фото", callback_data="photo"),
        InlineKeyboardButton("Текст", callback_data="text")
    ]
    markup.add(*buttons)
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text="Что нужно будет скинуть в качестве доказательств выполнения заданий?",
                                reply_markup=markup)

async def get_text(call: types.CallbackQuery):
    await redis.set("proof_type", call.data)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton('Отмена')
    markup.add(cancel)

    await bot.edit_message_text("Введите описания задания", call.message.chat.id, call.message.message_id, reply_markup=markup)
    await another_tasks_state.text.set()

async def get_quantity(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Спасибо!\n\n"
                         "Теперь введите количество")
    await bot.delete_message(message.chat.id, message.message_id)

async def get_price(message: types.Message, state: FSMContext):
    try:
        await state.update_data(quantity=int(message.text))
        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer("Спасибо!\n\n"
                             "Теперь введите желаемую цену")
        await another_tasks_state.next()
    except:
        await bot.delete_message(message.chat.id, message.message_id)

async def finish_fsm(message: types.Message, state: FSMContext):
    proof_type = await redis.get("proof_type")
    proof_type = proof_type.decode("utf-8")[0]

    data = await state.get_data()
    task_id = cur.execute("SELECT MAX(task_id) FROM telegram_channel_tasks").fetchone()[0]
    if task_id == None:
        task_id = 0

    price = float(message.text)

    dollar_balance = int(
        cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (message.from_user.id,)).fetchone()[0])
    if data["quantity"] * price <= dollar_balance:
        cur.execute('INSERT INTO another_tasks (task_id, proof_type, text, quantity, executed_quantity, price, who_did) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (task_id+1, proof_type, data['text'], data['quantity'], 0, price, ""))
        cur.execute('UPDATE users SET dollar_balance = (dollar_balance - ?) WHERE id = ?',
                    (data['quantity']*price, message.from_user.id))
        con.commit()

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Спасибо! Задания успешно выполнено")



async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Успешно отменено.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def reg(dp):
    dp.register_message_handler(cancel, lambda message: message.text == "Отмена", state="*")
    dp.register_callback_query_handler(create_task, text="another")
    dp.register_callback_query_handler(get_text, text=["photo", "text"])
    dp.register_message_handler(get_quantity, state=another_tasks_state.text)
    dp.register_message_handler(get_price, state=another_tasks_state.quantity)
    dp.register_message_handler(finish_fsm, state=another_tasks_state.price)