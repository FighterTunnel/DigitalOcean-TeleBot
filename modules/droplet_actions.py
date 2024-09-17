from telebot.types import CallbackQuery

import digitalocean

from _bot import bot
from utils.db import AccountsDB


def droplet_actions(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    droplet_id = data['droplet_id'][0]
    action = data['a'][0]

    try:
        account = AccountsDB().get(doc_id=doc_id)
        droplet = digitalocean.Droplet(
            token=account['token'],
            id=droplet_id
        )
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat mengambil akun atau droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    if action in globals():
        globals()[action](call, droplet)


def delete(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Menghapus droplet...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.destroy()
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat menghapus droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>✅ Droplet telah dihapus</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )


def shutdown(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Mematikan droplet, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.shutdown()
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat mematikan droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )


def reboot(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Merestart droplet, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.reboot()
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat merestart droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )


def power_on(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Menyalakan droplet, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.power_on()
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat menyalakan droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
def rebuild(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Membangun ulang droplet, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.rebuild()

    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat membangun ulang droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>✅ Droplet telah dibangun ulang</b>\n'
             f'🔑 Password baru dikirim ke email',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
def reset_password(call: CallbackQuery, droplet: digitalocean.Droplet):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>🔄 Mereset password droplet, silakan segarkan nanti</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode='HTML'
    )

    try:
        droplet.load()
        droplet.reset_root_password()
    except Exception as e:
        bot.edit_message_text(
            text=f'⚠️ Kesalahan saat mereset password droplet: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'<b>✅ Password droplet telah direset</b>\n'
             f'🔑 Password baru dikirim ke email',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )