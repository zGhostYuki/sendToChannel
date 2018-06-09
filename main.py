# Yuki's Project (C) 2018
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import re


updater = Updater('TOKEN')
dp = updater.dispatcher


def escape_m(txt):
    match_md = r'((([_*]).+?\3[^_*]*)*)([_*])'
    return re.sub(match_md, "\g<1>\\\\\g<4>", txt)


def fprint(string):
    with open("messages.log", "a") as f:
        f.write(string + "\n")


def error(err):
    fprint(err)


########################################################################################################################


def start(bot, update):
    cid = update.message.chat_id
    first_name = update.message.from_user.first_name
    uid = update.message.from_user.id
    bot.sendMessage(cid, "TEXT\n\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\nCreated by [t.me/zGhostYuki]\n"
                         "[Yuki's Project](t.me/YukisProject)",
                    'markdown', disable_web_page_preview=True)
    bot.sendMessage(IDFOUNDER, 'Started by [%s](tg://user?id=%s) \[%s]!' % (first_name, uid, uid), 'markdown',
                    disable_web_page_preview=True)


dp.add_handler(CommandHandler("start", start))


def send(bot, update):
    first_name = update.message.from_user.first_name
    uid = update.message.from_user.id
    cid = update.message.chat_id
    text = update.message.text
    bot.sendChatAction(cid, 'TYPING')
    if 't.me' in text:
        bot.sendMessage(chat_id=cid, text=f"You cannot send this link!", parse_mode='markdown')
        bot.sendMessage(chat_id=IDFOUNDER,
                        text=f"❗️ SPAM ALERT ❗️\n\n<[{first_name}](tg://user?id={uid}) - \[{uid}]>"
                             f" {text}", parse_mode='markdown')
    if '@' in text:
        bot.sendMessage(chat_id=cid, text=f"You cannot send this link!", parse_mode='markdown')
        bot.sendMessage(chat_id=IDFOUNDER,
                        text=f"❗️ SPAM ALERT ❗️\n\n<[{first_name}](tg://user?id={uid}) - \[{uid}]>"
                             f" {text}", parse_mode='markdown')
    else:
        if uid == IDFOUNDER:
            bot.sendMessage(chat_id=cid, text="*Inviato!*", parse_mode="markdown")
            bot.sendMessage(chat_id=IDFOUNDER, text=f"<[{first_name}](tg://user?id={uid}) - \[{uid}]> {text}",
                            parse_mode='markdown')
            bot.sendMessage(chat_id=CHANNELNICK, text=f"👑 {text}")
            fprint("Founder %s (%s): '%s'" % (first_name, uid, text))
            return

        bot.sendMessage(chat_id=cid, text="*Inviato!*", parse_mode="markdown")
        bot.sendMessage(chat_id=IDFOUNDER, text=f"<[{first_name}](tg://user?id={uid}) - \[{uid}]> {text}",
                        parse_mode='markdown')
        bot.sendMessage(chat_id=CHANNELNICK, text=f"👤 {text}")
        fprint("%s (%s): '%s'" % (first_name, uid, text))


dp.add_handler(MessageHandler(Filters.text, send))

########################################################################################################################


updater.start_polling(print('Bot started.'))
updater.idle()
