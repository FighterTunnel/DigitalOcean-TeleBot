from telebot.types import CallbackQuery

from _bot import bot
from utils.db import AccountsDB


def delete_account(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]

    try:
        AccountsDB().remove(doc_id=doc_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'{call.message.html_text}\n\n'
                 f'⚠️ Terjadi kesalahan saat menghapus akun: <code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             f'✅ <b>Akun berhasil dihapus</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
