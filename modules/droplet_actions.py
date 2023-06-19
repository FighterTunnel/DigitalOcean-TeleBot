from telebot.types import CallbackQuery

import digitalocean

from _bot import bot
from utils.db import AccountsDB


def droplet_actions(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    droplet_id = data['droplet_id'][0]
    action = data['a'][0]

    account = AccountsDB().get(doc_id=doc_id)
    droplet = digitalocean.Droplet(
        token=account['token'],
        id=droplet_id
    )

    if action in globals():
        globals()[action](call, droplet)


def delete(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Contoh Penghapusan...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    droplet.load()
    droplet.destroy()

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>Contoh telah dihapus</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )


def shutdown(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Dalam shutdown instance, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    droplet.load()
    droplet.shutdown()


def reboot(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Misalnya restart, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    droplet.load()
    droplet.reboot()


def power_on(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Dalam contoh, silakan menyegarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    droplet.load()
    droplet.reboot()
