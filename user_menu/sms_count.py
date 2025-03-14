from aiogram import types

from database import cur, con

# @dp.message_handler()
async def sms_count(msg: types.Message):
    info = cur.execute('SELECT * FROM users WHERE id = ?', (msg.from_user.id,))
    if info.fetchone() is None:
        cur.execute('INSERT INTO users (id, name, is_creator, dollar_balance, wallet_address, refs, invited) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (msg.from_user.id, msg.from_user.username, False, 0, "none", 0, 0))
        con.commit()
    # if len(msg.text) >= 30:
    cur.execute('UPDATE users SET dollar_balance = (dollar_balance + ?), name = ? WHERE id = ?',
                (1, msg.from_user.username, msg.from_user.id))
    con.commit()

    invited = cur.execute('SELECT invited FROM users WHERE id = ?', (msg.from_user.id,)).fetchone()[0]
    if invited != "none":
        cur.execute('UPDATE users SET dollar_balance = (dollar_balance + ?) WHERE id = ?',
                    (1, invited))
        con.commit()

def reg(dp):
    dp.register_message_handler(sms_count)