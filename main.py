from aiogram.utils import executor

import asyncio

from create_bot import dp
from user_menu import sms_count, leaderboard, fire, ref_system, send_mp_user
from user_menu.complete_the_task import subscribe_complete, boost_complete
from user_menu.private_messages import start_command, connect_wallet
from user_menu.tasks import create_another_task, create_tg_task
from admin_menu import ban, mute, send_mp_adm, admin_commands, giving_create_menu

connect_wallet.reg(dp)
ref_system.reg(dp)

ban.reg(dp)
mute.reg(dp)
leaderboard.reg(dp)
send_mp_user.reg(dp)
send_mp_adm.reg(dp)
start_command.reg(dp)
fire.reg(dp)
create_tg_task.reg(dp)
create_another_task.reg(dp)
admin_commands.reg(dp)
subscribe_complete.reg(dp)
boost_complete.reg(dp)
giving_create_menu.reg(dp)

sms_count.reg(dp)

if __name__ == '__main__':
    print("Bot is working")
    try:
        executor.start_polling(dp)
    except asyncio.TimeoutError:
        executor.start_polling(dp)