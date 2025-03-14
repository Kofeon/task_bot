from database import cur, con
from create_bot import bot

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import decode_payload


async def start_command(msg: types.Message):
    if msg.chat.type == "private":
        info = cur.execute('SELECT * FROM users WHERE id = ?', (msg.from_user.id,))
        if info.fetchone() is None:
            cur.execute('INSERT INTO users (id, name, is_creator, dollar_balance, wallet_address, refs, invited) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (msg.from_user.id, msg.from_user.username, False, 0, "none", 0, 0))
            con.commit()

            args = msg.get_args()
            if args:
                reference = decode_payload(args)
                cur.execute('UPDATE users SET refs = (refs + ?) WHERE id = ?',
                            (1, reference))
                cur.execute('UPDATE users SET invited = ? WHERE id = ?',
                            (reference, msg.from_user.id))
                con.commit()

        markup = InlineKeyboardMarkup(row_width=1)
        ref = InlineKeyboardButton("Реф ссылка", callback_data="ref")
        markup.add(ref)

        info = cur.execute('SELECT * FROM users WHERE id = ? AND wallet_address != ?', (msg.from_user.id, "none",))
        if info.fetchone() is None:
            markup.add(InlineKeyboardButton("Подключить кошелек", callback_data="connect"))
        else:
            markup.add(InlineKeyboardButton("Удалить кошелек", callback_data="del_wallet"))

        is_creator = cur.execute('SELECT is_creator FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0]
        if is_creator == True:
            markup.add(InlineKeyboardButton("Создать задание", callback_data="create_telegram_channel_tasks"))
        else:
            markup.add(InlineKeyboardButton("Доступные задания", callback_data="all_telegram_channel_tasks"))

        dollar_balance = int(cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
        # xp = int(cur.execute('SELECT xp FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
        wallet = str(cur.execute('SELECT wallet_address FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
        await bot.send_message(text='Привет!\n\n'
                                f'Баланс: <code>{dollar_balance}</code>$\n'
                                # f'Баланс XP: {xp}\n'
                                f'Адрес кошелька: <code>{wallet}</code>\n',
                                chat_id=msg.chat.id,
                                reply_markup=markup)

async def call_start_command(call: types.CallbackQuery):
    info = cur.execute('SELECT * FROM users WHERE id = ? AND wallet_address != ?', (call.from_user.id, "none"))
    if info.fetchone() is None:
        wallet_upd = InlineKeyboardButton("Подключить кошелек", callback_data="connect")
    else:
        wallet_upd = InlineKeyboardButton("Удалить кошелек", callback_data="del_wallet")

    markup = InlineKeyboardMarkup(row_width=1)
    ref = InlineKeyboardButton("Реф ссылка", callback_data="ref")
    create_telegram_channel_tasks = InlineKeyboardButton("Создать задание", callback_data="create_telegram_channel_tasks")
    get_telegram_channel_tasks = InlineKeyboardButton("Доступные задания", callback_data="all_telegram_channel_tasks")
    markup.add(wallet_upd, ref, create_telegram_channel_tasks, get_telegram_channel_tasks)

    dollar_balance = int(cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
    # xp = int(cur.execute('SELECT xp FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
    wallet = str(
        cur.execute('SELECT wallet_address FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
    await bot.send_message(text='Привет!\n\n'
                    f'Баланс: <code>{dollar_balance}</code>$\n'
                    # f'Баланс XP: {xp}\n'
                    f'Адрес кошелька: <code>{wallet}</code>\n',
                    chat_id=call.message.chat.id,
                    reply_markup=markup)

def reg(dp):
    dp.register_message_handler(start_command, commands=['start', 'restart'])
    dp.register_callback_query_handler(call_start_command, text=["main_menu", "cancel"])