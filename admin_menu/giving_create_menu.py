from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from create_bot import bot
from database import cur, con

class giving_create_menu(StatesGroup):
    creator_id = State()

async def get_creator_id(call: types.CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton('Отмена')
    markup.add(cancel)

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, "Введите id будущего создателя заданий:",
                                reply_markup=markup)
    await giving_create_menu.creator_id.set()

async def stop_gcm(msg: types.Message, state: FSMContext):
    await bot.delete_message(msg.chat.id, msg.message_id)
    cur.execute("UPDATE users SET is_creator = ? WHERE id = ?", (True, msg.text))
    con.commit()
    if cur.rowcount > 0:
        await bot.send_message(msg.chat.id,
                               "Спасибо!\n"
                               "Введенный пользователь успешно получил доступ к созданию заданий")
        await state.finish()
    else:
        await bot.send_message(msg.chat.id,
                               "Пользователь не найден. Пожалуйста, попробуйте еще раз или нажмите отмена")

async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Успешно отменено.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def reg(dp):
    dp.register_callback_query_handler(get_creator_id, text="giving_create_menu")
    dp.register_message_handler(stop_gcm, state=giving_create_menu.creator_id)
    dp.register_message_handler(cancel, lambda message: message.text == "Отмена", state="*")