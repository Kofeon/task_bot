from database import cur, con

from create_bot import dp, bot

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tonsdk.utils import Address

from pytonconnect import TonConnect
from pytonconnect.exceptions import TonConnectError


# @dp.callback_query_handler(text="connect_wallet")
async def connect(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Tonkeeper", callback_data="tonkeeper"),
        InlineKeyboardButton("MyTonWallet", callback_data="mytonwallet"),
        InlineKeyboardButton("TonHub", callback_data="tonhub")
    ]
    markup.add(*buttons)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Выберите ваш кошелек по ссылке ниже:", reply_markup=markup)

# @dp.callback_query_handler(text="tonkeeper")
async def connect_tonkeeper(call: types.CallbackQuery):
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/Kofeon/test/refs/heads/main/tonconnect-manifest.json')
    wallets_list = TonConnect.get_wallets()
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Подключить tonkeeper", url = await connector.connect(wallets_list[1])),
        InlineKeyboardButton("Отмена", callback_data="cancel")
    ]
    markup.add(*buttons)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Подключите кошелек по кнопке ниже", reply_markup=markup)
    result = await connector.wait_for_connection()
    if isinstance(result, TonConnectError):
        print('error:', result)
    else:
        if connector.connected and connector.account.address:
            cur.execute('UPDATE users SET wallet_address = ? WHERE id = ?',
                        (Address(connector.account.address).to_string(True, True, False),
                         call.from_user.id))
            con.commit()

            markup = InlineKeyboardMarkup(row_width=1)
            buttons = [
                InlineKeyboardButton("Удалить кошелек", callback_data="connect_wallet"),
                InlineKeyboardButton("Реф ссылка", callback_data="ref")
            ]

            markup.add(*buttons)

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
            await call.message.reply('Привет!\n\n'
                                     f'Баланс $: <code>{dollar_balance}</code>\n'
                                     # f'Баланс XP: {xp}\n'
                                     f'Адрес кошелька: <code>{wallet}</code>\n',
                                     reply_markup=markup)



# @dp.callback_query_handler(text="mytonwallet")
async def connect_mytonwallet(call: types.CallbackQuery):
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/Kofeon/test/refs/heads/main/tonconnect-manifest.json')
    wallets_list = TonConnect.get_wallets()
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Подключить MyTonWallet", url = await connector.connect(wallets_list[2])),
        InlineKeyboardButton("Отмена", callback_data="cancel")
    ]
    markup.add(*buttons)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Подключите кошелек по кнопке ниже", reply_markup=markup)
    result = await connector.wait_for_connection()
    if isinstance(result, TonConnectError):
        print('error:', result)
    else:
        if connector.connected and connector.account.address:
            cur.execute('UPDATE users SET wallet_address = ? WHERE id = ?',
                        (Address(connector.account.address).to_string(True, True, False),
                         call.from_user.id))
            con.commit()

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
            await call.message.reply('Привет!\n\n'
                                     f'Баланс $: <code>{dollar_balance}</code>\n'
                                     # f'Баланс XP: {xp}\n'
                                     f'Адрес кошелька: <code>{wallet}</code>\n',
                                     reply_markup=markup)

# @dp.callback_query_handler(text="tonhub")
async def connect_tonhub(call: types.CallbackQuery):
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/Kofeon/test/refs/heads/main/tonconnect-manifest.json')
    wallets_list = TonConnect.get_wallets()
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Подключить TonHub", url = await connector.connect(wallets_list[3])),
        InlineKeyboardButton("Отмена", callback_data="cancel")
    ]
    markup.add(*buttons)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Подключите кошелек по кнопке ниже", reply_markup=markup)
    result = await connector.wait_for_connection()
    if isinstance(result, TonConnectError):
        print('error:', result)
    else:
        if connector.connected and connector.account.address:
            cur.execute('UPDATE users SET wallet_address = ? WHERE id = ?',
                        (Address(connector.account.address).to_string(True, True, False),
                         call.from_user.id))
            con.commit()

            wallet_upd = InlineKeyboardButton("Удалить кошелек", callback_data="del_wallet")
            markup = InlineKeyboardMarkup(row_width=1)
            ref = InlineKeyboardButton("Реф ссылка", callback_data="ref")
            create_telegram_channel_tasks = InlineKeyboardButton("Создать задание", callback_data="create_telegram_channel_tasks")
            get_telegram_channel_tasks = InlineKeyboardButton("Доступные задания", callback_data="all_telegram_channel_tasks")
            markup.add(wallet_upd, ref, create_telegram_channel_tasks, get_telegram_channel_tasks)

            dollar_balance = int(cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
            # xp = int(cur.execute('SELECT xp FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
            wallet = str(cur.execute('SELECT wallet_address FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
            await call.message.reply('Привет!\n\n'
                            f'Баланс $: <code>{dollar_balance}</code>\n'
                            # f'Баланс XP: {xp}\n'
                            f'Адрес кошелька: <code>{wallet}</code>\n',
                            reply_markup=markup)

# @dp.callback_query_handler(text="del_wallet")
async def del_wallet(call: types.CallbackQuery):
    cur.execute('UPDATE users SET wallet_address = ? WHERE id = ?',
                ("none",
                 call.from_user.id))
    con.commit()

    await call.answer("Кошелек успешно удален", show_alert=True)

    wallet_upd = InlineKeyboardButton("Подключить кошелек", callback_data="connect")

    markup = InlineKeyboardMarkup(row_width=1)
    ref = InlineKeyboardButton("Реф ссылка", callback_data="ref")
    create_telegram_channel_tasks = InlineKeyboardButton("Создать задание", callback_data="create_telegram_channel_tasks")
    get_telegram_channel_tasks = InlineKeyboardButton("Доступные задания", callback_data="all_telegram_channel_tasks")
    markup.add(wallet_upd, ref, create_telegram_channel_tasks, get_telegram_channel_tasks)

    dollar_balance = int(cur.execute('SELECT dollar_balance FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
    # xp = int(cur.execute('SELECT xp FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0])
    wallet = str(cur.execute('SELECT wallet_address FROM users WHERE id = ?', (call.from_user.id,)).fetchone()[0])
    await call.message.reply('Привет!\n\n'
                    f'Баланс $: <code>{dollar_balance}</code>\n'
                    # f'Баланс XP: {xp}\n'
                    f'Адрес кошелька: <code>{wallet}</code>\n',
                    reply_markup=markup)

def reg(dp):
    dp.register_callback_query_handler(connect, text="connect")
    dp.register_callback_query_handler(connect_tonkeeper, text="tonkeeper")
    dp.register_callback_query_handler(connect_mytonwallet, text="mytonwallet")
    dp.register_callback_query_handler(del_wallet, text="del_wallet")