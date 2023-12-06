from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
def main_menu(check):
    kb = InlineKeyboardMarkup(row_width=1)
    instruction = InlineKeyboardButton(text="Видео-инструкция", callback_data="instruction")
    transaction = InlineKeyboardButton(text="Совершить перевод", callback_data="transaction")
    accept = InlineKeyboardButton(text="Подтвердить перевод", callback_data="accept")
    delete_trans = InlineKeyboardButton(text="Удалить заявку", callback_data="delete")
    kb.row(instruction)
    if check == True:
        kb.add(accept, delete_trans)
    else:
        kb.add(transaction)
    return kb
def main_menu_reply_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(mm)
    return kb
def delete_registration_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Да, удалить", callback_data="yes_delete")
    no = InlineKeyboardButton(text="Нет, не удалять", callback_data="no_delete")
    kb.row(yes, no)
    return kb
def main_admin_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    mailing = InlineKeyboardButton(text="Создать рассылку", callback_data="mailing")
    msg = InlineKeyboardButton(text="Написать пользователю", callback_data="send_message")
    end = InlineKeyboardButton(text="Завершить перевод", callback_data="end_tr")
    card = InlineKeyboardButton(text="Поменять карту", callback_data="change")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.row(mailing)
    kb.row(msg)
    kb.row(end)
    kb.row(card)
    kb.row(close)
    return kb
def canceling():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("Отмена❌")
    kb.add(cancel)
    return kb

def accept(id):
    kb = InlineKeyboardMarkup(row_width=1)
    copy = InlineKeyboardButton(text="Отправить чек")
    answer = InlineKeyboardButton(text="Написать пользователю", callback_data="send_message")
    kb.row(copy)
    return kb
def main_menu_call_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Главное меню", callback_data="main menu")
    kb.row(mm)
    return kb