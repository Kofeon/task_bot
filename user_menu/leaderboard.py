from database import cur

from aiogram import types

leaderboard_words = ["лидерборд", "leaderboard", "lb", "лб", "stats", "стата", "статистика"]

# @dp.message_handler(lambda message: message.text.lower() in leaderboard_words)
async def leaderboard(msg: types.Message):
    cur.execute("SELECT * FROM users ORDER BY dollar_balance DESC LIMIT ?", (10,))
    top_users = cur.fetchall()
    lb_user = ""
    for i in top_users:
        id, name, is_creator, dollar_balance, wallet, refs, invited = i
        dollar_balance = round(dollar_balance, 2)
        lb_user += f'<a href="https://t.me/{name}">{name}</a> -- {dollar_balance}\n'
    await msg.answer("Топ 10 среди всех пользователей:\n\n"
                     f'{lb_user}', disable_web_page_preview = True)

def reg(dp):
    dp.register_message_handler(leaderboard, lambda message: message.text.lower() in leaderboard_words)