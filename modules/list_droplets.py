from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import digitalocean

from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region


def list_droplets(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    t = '<b>VPS Manager</b>\n\n'

    account = AccountsDB().get(doc_id=doc_id)

    bot.edit_message_text(
        text=f'{t}'
             f'akun: <code>{account["email"]}</code>\n\n'
             'Detail Vps...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    droplets = digitalocean.Manager(token=account['token']).get_all_droplets()

    markup = InlineKeyboardMarkup()

    if len(droplets) == 0:
        markup.add(
            InlineKeyboardButton(
                text='Buat instance',
                callback_data=f'create_droplet?nf=select_region&doc_id={account.doc_id}'
            )
        )

        bot.edit_message_text(
            text=f'{t}'
                 f'akun: <code>{account["email"]}</code>\n\n'
                 'Tidak ada contoh',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    for droplet in droplets:
        markup.row(
            InlineKeyboardButton(
                text=f'{droplet.name} ({localize_region(droplet.region["slug"])}) ({droplet.size_slug})',
                callback_data=f'droplet_detail?doc_id={account.doc_id}&droplet_id={droplet.id}'
            )
        )

    bot.edit_message_text(
        text=f'{t}'
             f'akun: <code>{account["email"]}</code>\n\n'
             'Pilih contoh',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )
