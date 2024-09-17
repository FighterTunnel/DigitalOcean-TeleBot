from typing import Union

from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from _bot import bot
from utils.db import AccountsDB


def manage_droplets(d: Union[Message, CallbackQuery]):
    t = '<b>Manajer VPS</b>\n\n'
    markup = InlineKeyboardMarkup()

    accounts = AccountsDB().all()

    if len(accounts) == 0:
        markup.row(
            InlineKeyboardButton(
                text='➕ Tambah Akun',
                callback_data='add_account'
            )
        )

        bot.send_message(
            text=f'{t}'
                 f'⚠️ Tidak ada akun yang tersedia',
            chat_id=d.from_user.id,
            reply_markup=markup,
            parse_mode='HTML'
        )
        return

    for account in accounts:
        markup.add(
            InlineKeyboardButton(
                text=f'📧 {account["email"]}',
                callback_data=f'list_droplets?doc_id={account.doc_id}'
            )
        )

    bot.send_message(
        text=f'{t}'
             f'🔢 Pilih akun yang ingin dikelola',
        chat_id=d.from_user.id,
        parse_mode='HTML',
        reply_markup=markup
    )
