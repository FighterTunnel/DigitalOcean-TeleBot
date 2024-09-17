from typing import Union

from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from _bot import bot
from utils.db import AccountsDB


def manage_accounts(d: Union[Message, CallbackQuery]):
    t = '<b>Manajer Akun</b>\n\n'
    markup = InlineKeyboardMarkup()

    accounts = AccountsDB().all()

    if len(accounts) == 0:
        t += '⚠️ Tidak ada akun yang tersedia'
        markup.row(
            InlineKeyboardButton(
                text='➕ Tambahkan Akun Baru',
                callback_data='add_account'
            )
        )

        bot.send_message(
            text=t,
            chat_id=d.from_user.id,
            reply_markup=markup,
            parse_mode='HTML'
        )
        return

    markup.row(
        InlineKeyboardButton(
            text='🛠️ Uji Batch Akun',
            callback_data='batch_test_accounts'
        )
    )

    for account in accounts:
        markup.row(
            InlineKeyboardButton(
                text=f'📧 {account.get("email", "error")}',
                callback_data=f'account_detail?doc_id={account.doc_id}'
            )
        )

    bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        reply_markup=markup,
        parse_mode='HTML'
    )
