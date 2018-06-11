# Telegram @zGhostYuki (C) 2018

# Y88b   d88P        888      d8b d8b              8888888b.                   d8b                   888
#  Y88b d88P         888      Y8P 88P              888   Y88b                  Y8P                   888
#   Y88o88P          888          8P               888    888                                        888
#    Y888P  888  888 888  888 888 '  .d8888b       888   d88P 888d888 .d88b.  8888  .d88b.   .d8888b 888888
#     888   888  888 888 .88P 888    88K           8888888P'  888P'  d88''88b '888 d8P  Y8b d88P'    888
#     888   888  888 888888K  888    'Y8888b.      888        888    888  888  888 88888888 888      888
#     888   Y88b 888 888 '88b 888         X88      888        888    Y88..88P  888 Y8b.     Y88b.    Y88b.
#     888    'Y88888 888  888 888     88888P'      888        888     'Y88P'   888  'Y8888   'Y8888P  'Y888
#                                                                              888
#                                                                             d88P
#                                                                           888P'

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import re

updater = Updater('TOKEN')
dp = updater.dispatcher


def escape_m(txt):
    match_md = r'((([_*]).+?\3[^_*]*)*)([_*])'
    return re.sub(match_md, '\g<1>\\\\\g<4>', txt)


def fprint(string):
    with open('Files/messages.log', 'a') as f:
        f.write(string + '\n')


def error(err):
    fprint(err)


def register(uid):
    if str(uid) in open('Files/users.txt').read():
        return
    with open('Files/users.txt', 'a') as fl:
        fl.write(str(uid) + '\n')


def users(uid):
    try:
        return True if uid in [int(fuid) for fuid in open('Files/users.txt').readlines()] else False
    except Exception as err:
        print(err)


def ban(uid):
    with open('Files/banlist.txt', 'a') as fl:
        fl.write(str(uid) + '\n')


def banned(uid):
    try:
        return True if uid in [int(fuid) for fuid in open('Files/banlist.txt').readlines()] else False
    except Exception as err:
        print(err)


def adminadd(uid):
    with open('Files/admin.txt', 'a') as fl:
        fl.write(str(uid) + '\n')


def adminlist(uid):
    try:
        return True if uid in [int(fuid) for fuid in open('Files/admin.txt').readlines()] else False
    except Exception as err:
        print(err)


########################################################################################################################


def start(bot, update):
    cid = update.message.chat_id
    nick = update.message.from_user.username
    uid = update.message.from_user.id
    first_name = update.message.from_user.first_name
    if not nick:
        bot.sendMessage(cid,
                        f'TEXT\n\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\n'
                        f'Created by [Yuki](t.me/zGhostYuki)\n[Yuki\'s Project](t.me/YukisProject)',
                        'markdown', disable_web_page_preview=True)
        bot.sendMessage(cid, f'❗️ *WARNING* ❗️\nTo use the bot, *set a username* and press \'/start\'rt\'!',
                        'markdown')
        if str(uid) not in open('Files/users.txt').read():
            register(uid)
            bot.sendMessage(IDFOUNDER,
                            'Started by [%s](tg://user?id=%s) \[%s] for first time!' % (first_name, uid, uid),
                            'markdown', disable_web_page_preview=True)
        fprint(f'NoNick {first_name} ({uid}) started the bot for the first time.')
        print(f'NoNick {first_name} ({uid}) started the bot for the first time.')
    else:
        if banned(uid):
            bot.sendMessage(chat_id=cid, text='*You\'re banned from this bot!*', parse_mode='markdown')
            bot.sendMessage(chat_id=IDFOUNDER,
                            text=f'🚫 *Banned* [{nick}](tg://user?id={uid}) (`{uid}`) tried to send \'/start\'!',
                            parse_mode='markdown')
            fprint('Banned %s (%s) ha fatto \'/start\'!' % (nick, uid))
            print('Banned %s (%s) ha fatto \'/start\'!' % (nick, uid))
            return
        bot.sendMessage(cid,
                        f'TEXT\n\n\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\n'
                        f'Created by [Yuki](t.me/zGhostYuki)\n[Yuki\'s Project](t.me/YukisProject)',
                        'markdown', disable_web_page_preview=True)
        if str(uid) not in open('Files/users.txt').read():
            register(uid)
            bot.sendMessage(CHANNELNICK,
                            '<Bot> %s has started the bot! From this moment, he can sen messages here!' % nick,
                            'markdown', disable_web_page_preview=True)
            bot.sendMessage(IDFOUNDER, 'Started by [%s](tg://user?id=%s) \[%s] for first time!' % (nick, uid, uid),
                            'markdown', disable_web_page_preview=True)


dp.add_handler(CommandHandler('start', start))


def bancmd(bot, update, args):
    uid = update.message.from_user.id
    cid = update.message.chat_id
    nick = update.message.from_user.username
    try:
        if adminlist(uid):
            try:
                ban(args[0])
                update.message.reply_text(f'`{args[0]}` banned!', parse_mode='markdown')
                bot.sendMessage(args[0], f'You have been banned from this bot!')
                fprint(f'@{nick} [{uid}] added {args[0]} to banlist!')
                print('File banlist.txt updated.')
            except Exception as err:
                print(err)
        else:
            bot.sendMessage(chat_id=cid, text='You cannot use *this command*.', parse_mode='markdown')
    except Exception as err:
        print(err)


dp.add_handler(CommandHandler('ban', bancmd, pass_args=True))


def send(bot, update):
    first_name = update.message.from_user.first_name
    nick = update.message.from_user.username
    uid = update.message.from_user.id
    cid = update.message.chat_id
    text = update.message.text
    bot.sendChatAction(cid, 'TYPING')
    if not nick:
        bot.sendMessage(cid, f'To use the bot, *set a username*!', 'markdown')
        bot.sendMessage(IDFOUNDER, f'*NoNick* [{first_name}](tg://user?id={uid}) (`{uid}`) tried to send \'{text}\'.',
                        'markdown', disable_web_page_preview=True)
        fprint(f'NoNick {first_name} ({uid}) tried to send \'{text}\'.')
        print(f'NoNick {first_name} ({uid}) tried to send \'{text}\'.')
    else:
        if uid == IDFOUNDER:
            bot.sendMessage(chat_id=cid, text='*Sent!*', parse_mode='markdown')
            bot.sendMessage(chat_id=CHANNELNICK, text=f'👑 {text}', parse_mode='markdown',
                            disable_web_page_preview=True)
            fprint('Founder %s (%s): \'%s\'' % (nick, uid, text))
            print('Founder %s (%s): \'%s\'' % (nick, uid, text))
            return
        if adminlist(uid):
            bot.sendMessage(chat_id=cid, text='*Sent!*', parse_mode='markdown')
            bot.sendMessage(chat_id=IDFOUNDER, text=f'👮🏼 [{nick}](tg://user?id={uid}) (`{uid}`): {text}',
                            parse_mode='markdown')
            bot.sendMessage(chat_id=CHANNELNICK, text=f'👮🏼 {text}', parse_mode='markdown',
                            disable_web_page_preview=True)
            fprint('Admin %s (%s): \'%s\'' % (nick, uid, text))
            print('Admin %s (%s): \'%s\'' % (nick, uid, text))
            return
        if banned(uid):
            bot.sendMessage(chat_id=cid, text='*You\'re banned from this bot!*', parse_mode='markdown')
            bot.sendMessage(chat_id=IDFOUNDER,
                            text=f'🚫 *Banned* [{nick}](tg://user?id={uid}) (`{uid}`) tried to send \'{text}\'',
                            parse_mode='markdown')
            fprint('Banned %s (%s): \'%s\'' % (nick, uid, text))
            print('Banned %s (%s): \'%s\'' % (nick, uid, text))
            return
        bot.sendMessage(chat_id=cid, text='*Sent!*', parse_mode='markdown')
        bot.sendMessage(chat_id=IDFOUNDER, text=f'👤 [{nick}](tg://user?id={uid}) (`{uid}`): {text}',
                        parse_mode='markdown')
        bot.sendMessage(chat_id=CHANNELNICK, text=f'👤 {text}')
        fprint('%s (%s): \'%s\'' % (nick, uid, text))
        print('%s (%s): \'%s\'' % (nick, uid, text))


dp.add_handler(MessageHandler(Filters.text, send))


def admin(bot, update, args):
    uid = update.message.from_user.id
    cid = update.message.chat_id
    nick = update.message.from_user.username
    try:
        if uid == IDFOUNDER:
            try:
                adminadd(args[0])
                update.message.reply_text(f'`{args[0]}` is now admin!', parse_mode='markdown')
                bot.sendMessage(args[0], f'You are now an admin!')
                fprint(f'@{nick} [{uid}] added {args[0]} to admins!')
                print('File admin.txt updated.')
            except Exception as err:
                print(err)
        else:
            bot.sendMessage(chat_id=cid, text='You cannot use *this command*.',
                            parse_mode='markdown')
    except Exception as err:
        print(err)


dp.add_handler(CommandHandler('admin', admin, pass_args=True))

########################################################################################################################


updater.start_polling(print('Bot started.'))
updater.idle()
