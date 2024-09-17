from typing import Union

from telebot.types import (
    Message,
    CallbackQuery
)

import digitalocean
from digitalocean import DataReadError

from _bot import bot
from utils.db import AccountsDB
from .start import start


def add_account(d: Union[Message, CallbackQuery]):
    t = '<b>🔑 Tambahkan Akun DigitalOcean</b>\n\n' \
        'Masukkan Token DigitalOcean <a href="https://cloud.digitalocean.com/account/api/tokens">Ambil Disini</a> perhatikan dalam copy paste\n\n' \
        'Contoh:\n' \
        '<code>token123:Komentarxxx</code>\n' \
        '<code>token345</code>\n\n' \
        '/cancel untuk membatalkan'

    msg = bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

    bot.register_next_step_handler(msg, add_account_next_step_handler)


def add_account_next_step_handler(m: Message):
    if m.text == '/cancel':
        start(m)
        return

    msg = bot.send_message(
        text='🔄 Menambahkan akun...',
        chat_id=m.from_user.id
    )

    accounts = m.text.split('\n')
    added_accounts = []
    failed_accounts = []

    for account in accounts:
        if ':' in account:
            token = account.split(':')[0]
            remarks = account.split(':')[1]
        else:
            token = account
            remarks = ''

        try:
            email = digitalocean.Account().get_object(
                api_token=token
            ).email

            AccountsDB().save(
                email=email,
                token=token,
                remarks=remarks
            )

            added_accounts.append(email)

        except DataReadError:
            failed_accounts.append(account)
        except Exception as e:
            bot.edit_message_text(
                text=f'⚠️ Kesalahan saat menambahkan akun: <code>{str(e)}</code>',
                chat_id=m.from_user.id,
                message_id=msg.message_id,
                parse_mode='HTML'
            )
            return

    t = f'<b>📊 Total {len(accounts)} akun</b>\n\n'

    if added_accounts:
        t += f'✅ Berhasil menambahkan {len(added_accounts)} akun:\n'
        for added_account in added_accounts:
            t += f'<code>{added_account}</code>\n'
        t += '\n'

    if failed_accounts:
        t += f'❌ Gagal menambahkan {len(failed_accounts)} akun:\n'
        for failed_account in failed_accounts:
            t += f'<code>{failed_account}</code>\n'

    bot.edit_message_text(
        text=t,
        chat_id=m.from_user.id,
        message_id=msg.message_id,
        parse_mode='HTML'
    )
