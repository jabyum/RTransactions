import telebot
import buttons as bt
import database as db
import time
import threading
from telebot import types
bot = telebot.TeleBot("6571509666:AAHfeZFsPDIoz4Dj9DFBUEgDrpvf3S4D2CU")


@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id
    channel_id = -1002117108600
    check_registration = db.check_user(user_id)
    check = db.check(user_id)
    if check_registration == False:
        db.reg_user(user_id)
    try:
        member = bot.get_chat_member(channel_id, user_id)
        if member.status != "left":
            mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
            bot.delete_message(user_id, mm.message_id)
            bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu(check))
        else:
            bot.send_message(user_id, "Подпишитесь на канал,чтобы пользоваться ботом \nhttps://t.me/russiantransaction",
                             reply_markup=bt.check_menu_call_kb())
    except:
        pass

@bot.callback_query_handler(lambda call: call.data in ["instruction", "transaction", "accept",
                                                       "delete", "no_delete", "yes_delete", "mailing",
                                                       "send_message", "change", "end_tr", "main menu",
                                                       "check menu"])
def calling(call):
    user_id = call.message.chat.id
    if call.data == "instruction":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "ссылка на видео")
    elif call.data == "check menu":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Вы успешно подписались ✅")
        return start_message(call)
    elif call.data == "main menu":
        return start_message(call)
    elif call.data == "transaction":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Какую сумму вы хотите перевести?", reply_markup=bt.main_menu_reply_kb())
        bot.register_next_step_handler(call.message, get_sum)
    elif call.data == "accept":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "↗️ Отправьте скриншот/фото подтверждения перевода", reply_markup=bt.main_menu_reply_kb())
        bot.register_next_step_handler(call.message, get_photo)
    elif call.data == "delete":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Вы уверены, что хотите удалить свою заявку?",
                         reply_markup=bt.delete_registration_kb())
    elif call.data == "no_delete":
        bot.delete_message(user_id, call.message.message_id)
        return start_message(call)
    elif call.data == "yes_delete":
        try:
            bot.delete_message(user_id, call.message.message_id)
            db.delete_transaction(user_id)
            bot.send_message(user_id, "Ваша заявка удалена")
            start_message(call)
        except:
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "❗️ Произошла ошибка. Обратиться в службу поддержки ❗️")
            return start_message(call)
    elif call.data == "mailing":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Введите текст рассылки или отправьте фотографию с описанием, либо отмените рассылку через кнопку в меню",
                         reply_markup=bt.canceling())
        bot.register_next_step_handler(call.message, mailing_to_all)
    elif call.data == "send_message":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Введите айди пользователя, которому вы хотите написать",
                         reply_markup=bt.canceling())
        bot.register_next_step_handler(call.message, send_answer)
    elif call.data == "change":
        bot.delete_message(user_id, call.message.message_id)
        actual_card = db.get_card()
        bot.send_message(user_id, f"Акутальная карта на данный момент: 💳 {actual_card}\n\n"
                                  f"Введите номер новой карты или нажмите кнопку отмены",
                         reply_markup=bt.canceling())
        bot.register_next_step_handler(call.message, get_new_card)
    elif call.data == "end_tr":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Введите ID пользователя для завершения перевода или нажмите кнопку отмены",
                         reply_markup=bt.canceling())
        bot.register_next_step_handler(call.message, get_id_end)
def get_id_end(message):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            user_id = int(message.text)
            bot.send_message(admin_id, "Отправьте фото потверждения перевода ↗️", reply_markup=bt.canceling())
            bot.register_next_step_handler(message, get_photo_end, user_id)
        except:
            bot.send_message(admin_id, "Неправильный айди", reply_markup=types.ReplyKeyboardRemove())
def get_photo_end(message, user_id):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        bot.send_photo(user_id, photo=photo, caption=message.caption)
        bot.send_message(admin_id, "Перевод подтвержден ✅. Заявка удалена", reply_markup=types.ReplyKeyboardRemove())
        db.delete_transaction(user_id)
    else:
        text = message.text
        try:
            bot.send_message(user_id, text)
            bot.send_message(admin_id, "Ответ отправлен. Заявка удалена", reply_markup=types.ReplyKeyboardRemove())
            db.delete_transaction(user_id)
        except:
            bot.send_message(admin_id, "Не удалось отправить ответ: заявка удалена или пользователь удалил бота",
                             reply_markup=types.ReplyKeyboardRemove())
def get_new_card(message):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            new_card = message.text
            db.delete_card()
            db.reg_card(new_card)
            bot.send_message(admin_id, f"Вы поменяли номер карты. Новый номер: 💳 {new_card}", reply_markup=types.ReplyKeyboardRemove())
        except:
            bot.send_message(admin_id, "Ошибка", reply_markup=types.ReplyKeyboardRemove())


def send_message_to_user(target_id, text, photo):
    target = target_id[0]
    if photo == None:
        try:
            time.sleep(0.2)
            bot.send_message(target, text)
        except:
            pass
    else:
        try:
            time.sleep(0.2)
            bot.send_photo(target_id, photo=photo, caption=text)
        except:
            pass


def mailing_to_all(message):
    user_id = message.from_user.id
    targets_id = db.mailing_all()
    if message.text == "Отмена❌":
        bot.send_message(user_id, "Рассылка отменена", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        text = message.caption
        for target_id in targets_id:
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    else:
        for target_id in targets_id:
            text = message.text
            photo = None
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    bot.send_message(user_id, "Рассылка завершена", reply_markup=types.ReplyKeyboardRemove())
    admin_panel(message)
def get_photo(message):
    user_id = message.from_user.id
    if message.photo:
        try:
            photo = message.photo[-1].file_id
            information = db.get_user(user_id)
            bot.send_message(user_id, "Подтверждение отправлено. Ждите ответа",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.send_photo(305896408, photo=photo, caption=f"<b>Заявка № {information[0]}</b>\n"
                                                           f"🆔 клиента: <code>{information[1]}</code>\n"
                                                           f"💵 Зарегестрированная сумма перевода: {information[2]}\n"
                                                           f"💳 Номер карты: <code>{information[3]}</code>",
                           parse_mode="html")
            try:
                bot.send_photo(3356664, photo=photo, caption=f"<b>Заявка № {information[0]}</b>\n"
                                                               f"🆔 клиента: <code>{information[1]}</code>\n"
                                                               f"💵 Зарегестрированная сумма перевода: {information[2]}\n"
                                                               f"💳 Номер карты: <code>{information[3]}</code>",
                               parse_mode="html")
            except:
                pass

            try:
                bot.send_photo(575148251, photo=photo, caption=f"<b>Заявка № {information[0]}</b>\n"
                                                               f"🆔 клиента: <code>{information[1]}</code>\n"
                                                               f"💵 Зарегестрированная сумма перевода: {information[2]}\n"
                                                               f"💳 Номер карты: <code>{information[3]}</code>",
                               parse_mode="html")
            except:
                pass
        except:
            bot.send_message(user_id, "❗️ Ошибка. Повторите заново ❗️")
    elif message.text == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте фотографию подтверждения", reply_markup=bt.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_photo)
def get_sum(message):
    user_id = message.from_user.id
    money = message.text
    if money == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "💳 Отправьте номер карты получателя", reply_markup=bt.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_cardnum, money)
def get_cardnum(message, money):
    user_id = message.from_user.id
    cardnum = message.text
    check = db.check(user_id)
    if check == True:
        bot.send_message(user_id, "Ошибка. У вас уже имеется активная заявка")
    else:
        if cardnum == "Главное меню":
            start_message(message)
        else:
            try:
                card = db.get_card()
                bot.send_message(user_id, f"Заявка принята✅.\n Переведите указанную вами сумму на карту "
                                          f"сбербанка(кликните, чтобы скопировать) 💳 <code>{card}</code>, "
                                          f"затем отправьте скриншот перевода в качестве подтверждения\n"
                                          f"Перевод можно подтвердить в главном меню ⬇️", parse_mode="html",
                                 reply_markup=bt.main_menu_call_kb())
                db.register_transaction(user_id, money, cardnum)
            except:
                bot.send_message(user_id, "❗️ Ошибка. Повторите заново ❗️")
def send_answer(message):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            user_id = int(message.text)
            bot.send_message(admin_id, "Введите сообщения для пользователя", reply_markup=bt.canceling())
            bot.register_next_step_handler(message, send_full_answer, user_id)
        except:
            bot.send_message(admin_id, "Неправильный айди", reply_markup=types.ReplyKeyboardRemove())
def send_full_answer(message, user_id):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        bot.send_photo(user_id, photo=photo, caption=message.caption)
        bot.send_message(admin_id, "Ответ отправлен", reply_markup=types.ReplyKeyboardRemove())
    else:
        text = message.text
        try:
            bot.send_message(user_id, text)
            bot.send_message(admin_id, "Ответ отправлен", reply_markup=types.ReplyKeyboardRemove())
        except:
            bot.send_message(admin_id, "Не удалось отправить ответ", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["admin"])
def admin_panel(message):
    user_id = message.from_user.id
    checker = 305896408
    types.ReplyKeyboardRemove()
    if user_id == checker or user_id == 575148251 or user_id == 3356664:
        bot.send_message(user_id, "Админ панель. Выберите действие",
                         reply_markup=bt.main_admin_menu())
    else:
        pass

bot.infinity_polling()