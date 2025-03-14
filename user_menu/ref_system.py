from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import cur




async def ref_command(call: types.CallbackQuery):
    refs = cur.execute('SELECT refs FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0]

    link = await get_start_link(call.from_user.id, encode=True)
    markup = InlineKeyboardMarkup()
    mm = InlineKeyboardButton("Главное меню", callback_data="main_menu")
    markup.add(mm)
    await call.message.edit_text(f"Приглашайте людей и получайте 50% с их заработка в points\n"
                         f"На данный момент у вас {refs} рефералов\n\n"
                         f"<code>{link}</code>\n\n",
                                 reply_markup=markup)



def reg(dp):
    dp.register_callback_query_handler(ref_command, text="ref")