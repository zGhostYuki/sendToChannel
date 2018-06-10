# Yuki's Project (C) 2018
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import re


updater = Updater('TOKEN')
dp = updater.dispatcher


def escape_m(txt):
    match_md = r'((([_*]).+?\3[^_*]*)*)([_*])'
    return re.sub(match_md, "\g<1>\\\\\g<4>", txt)


def fprint(string):
    with open("Files/messages.log", "a") as f:
        f.write(string + "\n")


def error(err):
    fprint(err)


def banned(uid):
    try:
        return True if uid in [int(fuid) for fuid in open("Files/banlist.txt").readlines()] else False
    except Exception as err:
        print(err)


def banna(uid):
    with open("Files/banlist.txt", "a") as fl:
        fl.write(str(uid) + "\n")


def register(uid):
    if str(uid) in open("Files/users.txt").read():
        return
    with open("Files/users.txt", "a") as fl:
        fl.write(str(uid) + "\n")


########################################################################################################################


def start(bot, update):
    cid = update.message.chat_id
    first_name = update.message.from_user.first_name
    uid = update.message.from_user.id
    if banned(uid):
        bot.sendMessage(chat_id=cid, text="*You're banned from this bot!*", parse_mode="markdown")
        bot.sendMessage(chat_id=IDFOUNDER, text=f"*[Banned]* [{first_name}](tg://user?id={uid}) \[`{uid}`] tryed to"
                                                f" do \'/start\'!",
                        parse_mode='markdown')
        fprint("Banned %s (%s) sent '/start'!" % (first_name, uid))
        return
    bot.sendMessage(cid,"TEXT\n\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\nCreated by [Yuki](t.me/zGhostYuki)"
                         "\n[Yuki's Project](t.me/YukisProject)", 'markdown', disable_web_page_preview=True)
    bot.sendMessage(197896791, 'Started by [%s](tg://user?id=%s) \[%s]!' % (nick, uid, uid), 'markdown',
                    disable_web_page_preview=True)
    if str not in open("Files/users.txt").read():
        bot.sendMessage(CHANNELNICK, '<Bot> %s started the bot! From now he can write in this channel!' % nick,
                        'markdown', disable_web_page_preview=True)
        bot.sendMessage(IDFOUNDER, 'Started by [%s](tg://user?id=%s) \[%s] for first time!' % (nick, uid, uid),
                        'markdown', disable_web_page_preview=True)


dp.add_handler(CommandHandler("start", start))


def ban(bot, update, args):
    uid = update.message.from_user.id
    cid = update.message.chat_id
    nick = update.message.from_user.username
    try:
        if uid == IDFOUNDER:
            try:
                banna(args[0])
                update.message.reply_text(f"`{args[0]}` banned!", parse_mode='markdown')
                bot.sendMessage(args[0], f"You have been banned from this bot!")
                fprint(f"@{nick} [{uid}] banned {args[0]}!")
                print('File banlist.txt updated.')
            except Exception as err:
                print(err)
        else:
            bot.sendMessage(chat_id=cid, text="You cannot use *this command*!",
                            parse_mode='markdown')
    except Exception as err:
        print(err)


dp.add_handler(CommandHandler("ban", ban, pass_args=True))


def send(bot, update):
    first_name = update.message.from_user.first_name
    uid = update.message.from_user.id
    cid = update.message.chat_id
    text = update.message.text
    bot.sendChatAction(cid, 'TYPING')
    if 't.me' in text:
        bot.sendMessage(chat_id=cid, text=f"You cannot send this link!", parse_mode='markdown')
        bot.sendMessage(chat_id=IDFOUNDER,
                        text=f"❗️ SPAM ALERT ❗️\n\n<[{nick}](tg://user?id={uid}) - \[`{uid}`]>"
                             f" {text}", parse_mode='markdown')
    if '@' in text:
        bot.sendMessage(chat_id=cid, text=f"You cannot send this username!", parse_mode='markdown')
        bot.sendMessage(chat_id=IDFOUNDER,
                        text=f"❗️ SPAM ALERT ❗️\n\n[{nick}](tg://user?id={uid}) - \[`{uid}`]:"
                             f" {text}", parse_mode='markdown')
    else:
        if uid == IDFOUNDER:
            bot.sendMessage(chat_id=cid, text="*Sent!*", parse_mode="markdown")
            bot.sendMessage(chat_id=CHANNELNICK, text=f"*[Founder]* <{nick}> {text}", parse_mode='markdown',
                            disable_web_page_preview=True)
            fprint("Founder %s (%s): '%s'" % (first_name, uid, text))
            return
        if banned(uid):
            bot.sendMessage(chat_id=cid, text="*You're banned from this bot!*", parse_mode="markdown")
            bot.sendMessage(chat_id=IDFOUNDER, text=f"*[Banned]* [{nick}](tg://user?id={uid}) \[`{uid}`] tryed"
                                                    f" to send \'{text}\'", parse_mode='markdown')
            fprint("Banned %s (%s) tryed to send \'%s\'" % (first_name, uid, text))
            return
        bot.sendMessage(chat_id=cid, text="*Sent!*", parse_mode="markdown")
        bot.sendMessage(chat_id=IDFOUNDER, text=f"[{nick}](tg://user?id={uid}) \[`{uid}`]: {text}",
                        parse_mode='markdown')
        bot.sendMessage(chat_id=CHANNELNICK, text=f"<{nick}> {text}")
        fprint("%s (%s): '%s'" % (first_name, uid, text))


dp.add_handler(MessageHandler(Filters.text, send))

########################################################################################################################


updater.start_polling(print('Bot started.'))
updater.idle()
