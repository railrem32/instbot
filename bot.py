import telebot
import db
import config
import executor

bot = telebot.TeleBot(config.CONST_TOKEN)


def extract_arg(arg):
    return arg.split()[1:]

def check_args(args,chat_id,err_message='Не забывай передавать имя пользователя!',length=1):
    if (args is None or len(args) < length):
        bot.send_message(chat_id, err_message)
        return False
    return True
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне\nЕсли в первый раз начни с /set')

@bot.message_handler(commands=['set'])
def set_message(message):
    args = extract_arg(message.text)
    if (not check_args(args,message.chat.id,'Не забывай передевать логин и пароль через прообел!!!',2)):
        return
    db.set_user_settings(message.from_user.id,args[0],args[1])
    bot.send_message(message.chat.id, 'Обновил (Поднял, обнял, заплакал)')

@bot.message_handler(commands=['run'])
def run_message(message):
    args = extract_arg(message.text)
    if (not check_args(args, message.chat.id)):
        return
    target_account = args[0]
    user = db.get_user_settings(message.from_user.id)
    if (user is None):
        bot.send_message(message.chat.id, 'Настрой логин и пароль !!! /set')
    else:
        db.create_task(target_account,message.chat.id,message.from_user.id)
        bot.send_message(message.chat.id, 'Задание принято в обработку \nСтатус можно узнать через /status')
        errmessage = executor.run()
        if errmessage is not None :
             bot.send_message(message.chat.id, errmessage)

@bot.message_handler(commands=['unfollow'])
def run_message(message):
    args = extract_arg(message.text)
    if (not check_args(args, message.chat.id)):
        return
    target_account = args[0]
    user = db.get_user_settings(message.from_user.id)
    if (user is None):
        bot.send_message(message.chat.id, 'Настрой логин и пароль !!! /set')
    else:
        db.create_task(target_account,message.chat.id,message.from_user.id)
        bot.send_message(message.chat.id, 'Задание принято в обработку \nСтатус можно узнать через /status')
        errmessage = executor.run(isUnfollow=True)
        if errmessage is not None :
             bot.send_message(message.chat.id, errmessage)


@bot.message_handler(commands=['likers'])
def run_message(message):
    args = extract_arg(message.text)
    if (not check_args(args, message.chat.id,"Не забывай передевать (профиль)  (кол-во лайкеров) (кол-во фото пользователя)!!!",3)):
        return
    target_account = args[0]
    likers = args[1]
    photos = args[2]

    user = db.get_user_settings(message.from_user.id)
    if (user is None):
        bot.send_message(message.chat.id, 'Настрой логин и пароль !!! /set')
    else:
        db.create_task(target_account,message.chat.id,message.from_user.id)
        bot.send_message(message.chat.id, 'Задание принято в обработку \nСтатус можно узнать через /status')
        errmessage = executor.run(True,photos,likers)
        if errmessage is not None :
             bot.send_message(message.chat.id, errmessage)


@bot.message_handler(commands=['cancel'])
def cancel_message(message):
    args = extract_arg(message.text)
    if (not check_args(args, message.chat.id)):
        return
    target_account = args[0]
    task = db.get_task_status(message.from_user.id,message.chat.id,target_account)
    task_status = task.get(db.FIELD_STATUS)
    if (task_status == db.CONST_STATUS_NEW):
        db.update_task_status(target_account,message.from_user.id,db.CONST_STATUS_FINISHED)
        bot.send_message(message.chat.id, 'Задание отменено')
    else :
        bot.send_message(message.chat.id, 'Задание уже нельзя отменить')

@bot.message_handler(commands=['status'])
def status_message(message):
    args = extract_arg(message.text)
    if (not check_args(args,message.chat.id)):
        return
    v = db.get_task_status(message.from_user.id,message.chat.id,args[0]).get(db.FIELD_STATUS)
    result='хз чет пошло не так'
    if (v == db.CONST_STATUS_NEW):
        result = 'в очереди'
    if (v == db.CONST_STATUS_FAILED):
        result = 'упало с ошибкой'
    if (v == db.CONST_STATUS_FINISHED):
        result = 'завершено'
    if (v == db.CONST_STATUS_INPROCESS):
        result = 'в обработке'
    bot.send_message(message.chat.id, 'Задание по {} {}'.format(args[0],result))

bot.polling()

