from telebot.types import CallbackQuery

import digitalocean
from digitalocean import DataReadError

from _bot import bot
from utils.db import AccountsDB


def batch_test_delete_accounts(call: CallbackQuery):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>Hapus Akun Kegagalan...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    accounts_db = AccountsDB()

    accounts = accounts_db.all()
    for account in accounts:
        try:
            digitalocean.Balance().get_object(api_token=account['token'])

        except DataReadError:
            accounts_db.remove(doc_id=account.doc_id)

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>Akun kegagalan yang dihapus</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
