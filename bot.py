import random


import telebot
from telebot import types
from dotenv import dotenv_values, load_dotenv


from users import *


class BotCommands:
    START = 'start'
    HELP = 'help'
    CARDS = 'cards'
    NEW_CARD = 'new_card'
    DELETE_CARD = 'delete_card'
    TRAINING = 'traning'


config = dotenv_values(".env")
load_dotenv()
token = config["TG_TOKEN"]
BOT = telebot.TeleBot(token)

def run_bot():
    global BOT
    if not init_users():
        print('Error init users')
        exit(1)
    print('Бот запущен...')
    print('Для завершения нажмите Ctrl+C')
    BOT.polling()



def get_reply_keyboard_markup(commands=[BotCommands.HELP, BotCommands.CARDS, BotCommands.NEW_CARD, BotCommands.DELETE_CARD, BotCommands.TRAINING], one_time_keyboard=False):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=one_time_keyboard)
    for command in commands:
        markup.add(f'/{command}')
    return markup



@BOT.message_handler(commands=[BotCommands.START])
def start_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        cretate_ok = create_user(user_id)
        if cretate_ok:
            response = f"STARTING\nHello, let's start!\nPrint /{BotCommands.HELP} to see help"
        else:
            request_from_non_exits_user_processing(message)
            set_user_state(user_id, UserStates.NOT_CREATED)
            return
    else:
        response = f"STARTING\nHello, let's continue!\nPrint /{BotCommands.HELP} to see help if forgot"

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


@BOT.message_handler(commands=[BotCommands.HELP])
def help_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return

    response = f'''
    HELP\nThis is LearnCardBot.\nCreate cards with <Key>-<Value>: <word or phrase> - <translation or meaning>.\nThen learn them in training mode.
    /{BotCommands.HELP} - this help
    /{BotCommands.CARDS} - show your cards
    /{BotCommands.NEW_CARD} - add new card to learn
    /{BotCommands.DELETE_CARD} - delete card from learn
    /{BotCommands.TRAINING} - traning your cards
    '''

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


@BOT.message_handler(commands=[BotCommands.CARDS])
def show_cards_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return

    cards = get_user_cards_with_meanings(user_id)
    output_cards = ''
    if cards is None:
        response = "CARDS\nSorry, smth went wrong while getting cards"
    else:
        i = 1
        for cortege in cards:
            output_cards += str(i) + '. ' + cortege[0] + ' <---> ' + cortege[1] + '\n'
            i += 1
        response = f"CARDS:\n" + output_cards

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


@BOT.message_handler(commands=[BotCommands.NEW_CARD])
def create_card_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return
    response = "CREATING\nCard is <KEY>-<VALUE> pair.\nWrite <KEY> for new card"
    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup(commands=[]))
    set_user_state(user_id, UserStates.REQUEST_NEW_CARD)


@BOT.message_handler(commands=[BotCommands.DELETE_CARD])
def delete_card_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return
    response = "DELETING\nCard is <KEY>-<VALUE> pair.\nWrite <KEY> to delete it"
    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup(commands=[]))
    set_user_state(user_id, UserStates.REQUEST_DELETE_CARD)


@BOT.message_handler(commands=[BotCommands.TRAINING])
def traning_handler(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return
    request_trainig_processing(message)


@BOT.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = get_user_id_by_message(message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(message)
        return

    if message.content_type == 'text':
        state = get_user_state(user_id)
        if state == UserStates.MENU:
            request_menu_processing(message)
        elif state == UserStates.REQUEST_NEW_CARD:
            request_new_card_processing(message)
        elif state == UserStates.REQUEST_NEW_CARD_MEANING:
            request_new_card_meaning_processing(message)
        elif state == UserStates.REQUEST_DELETE_CARD:
            request_delete_card_processing(message)
        elif state == UserStates.REQUEST_DELETE_CARD_CONFIRM:
            request_delete_card_confirm_processing(message)
        elif state == UserStates.REQUEST_TRAINING:
            request_trainig_processing(message)
        else:
            BOT.reply_to(message, f"ECHO_MODE\nUndefined state\nTry use /{BotCommands.HELP}", reply_markup=get_reply_keyboard_markup())
            set_user_state(user_id, UserStates.MENU)
    else:
        BOT.reply_to(message, f"ECHO_MODE\nUndefined content type\nTry use /{BotCommands.HELP}", reply_markup=get_reply_keyboard_markup())
        set_user_state(user_id, UserStates.MENU)



def request_from_non_exits_user_processing(message):
    user_id = get_user_id_by_message(message)
    response = f"STARTING\nLet's start!\nPrint /{BotCommands.START}"
    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup(commands=[BotCommands.START]))


def request_menu_processing(message):
    user_id = get_user_id_by_message(message)
    response = f"MENU\nLet's choose what you want (use /{BotCommands.HELP} if forgot)"
    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


def request_new_card_processing(message):
    user_id = get_user_id_by_message(message)
    new_state = UserStates.MENU
    new_card = message.text
    is_exist = is_user_card_exist(user_id, new_card)
    if is_exist is None:
        response = "CREATING\nSorry, smth went wrong while checking is card exist:\n'" + new_card + "'"
    else:
        if is_exist:
            meaning = get_user_card_meaning(user_id, new_card)
            if meaning is None:
                response = "CREATING\nCard already exist, but can't get meaning:\n'" + new_card + "'"
            else:
                response = "CREATING\nCard already exist:\n'" + new_card + "'\nwith meaning:\n'" + meaning + "'"
        else:
            response = "CREATING\nYou want to add new card:\n'" + new_card+ "'\nWrite translation or meaning for it"
            set_user_add_card(user_id, new_card)
            new_state = UserStates.REQUEST_NEW_CARD_MEANING

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup(commands=[]))
    set_user_state(user_id, new_state)


def request_new_card_meaning_processing(message):
    user_id = get_user_id_by_message(message)
    new_card = get_user_add_card(user_id)
    new_card_meaning = message.text
    create_ok, count = create_user_card(user_id, new_card, new_card_meaning)
    if create_ok:
        response = f"CREATING\nOK. You added new card:\n'" + new_card + "'\nwith meaning:\n'" + new_card_meaning + "'\n" \
        + str(count) + " cards in your list now"
    else:
        response = "CREATING\nSorry, smth went wrong while creating new card:\n'" + new_card + "'"

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


def request_delete_card_processing(message):
    user_id = get_user_id_by_message(message)
    new_state = UserStates.MENU
    delete_card = message.text
    is_card_exist = is_user_card_exist(user_id, delete_card)
    if is_card_exist is None:
        response = "DELETING\nSorry, smth went wrong. Can't find card:\n'" + delete_card + "'"
    else:
        if not is_card_exist:
            response = "DELETING\nCard not found:\n'" + delete_card + "'"
        else:
            delete_card_meaning = get_user_card_meaning(user_id, delete_card)
            if delete_card_meaning is None:
                response = "DELETING\nSorry, smth went wrong. Can't find card meaning, but card exist:\n'" + delete_card + "'"
            else:
                response = "DELETING\nYou want to delete card:\n'" + delete_card + "'\nwith meaning:\n'" + delete_card_meaning + f"'\nIf you are sure, write {UserAnswerVariants.CONFIRM_DELETE} or use base commands to change operation"
                set_user_delete_card(user_id, delete_card)
                new_state = UserStates.REQUEST_DELETE_CARD_CONFIRM

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup(commands=[]))
    set_user_state(user_id, new_state)


def request_delete_card_confirm_processing(message):
    user_id = get_user_id_by_message(message)
    if message.text == UserAnswerVariants.CONFIRM_DELETE:
        delete_card = get_user_delete_card(user_id)
        delete_ok = delete_user_card(message.chat.id, delete_card)
        if delete_ok is None:
            response = "DELETING\nSorry, smth went wrong while deleting card:\n'" + delete_card + "'"
        else:
            if delete_ok:
                response = "DELETING\nCard is deleted:\n'" + delete_card + "'"
            else:
                response = "DELETING\nSorry, smth went wrong. Cant't delete card:\n'" + delete_card + "'"
    else:
        response = "DELETING\nCard is not deleted. Canceled"

    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())
    set_user_state(user_id, UserStates.MENU)


def request_trainig_processing(message):
    user_id = get_user_id_by_message(message)
    if get_user_state(user_id) != UserStates.REQUEST_TRAINING:
        cards = get_user_cards_with_meanings(user_id)
        set_user_cached_cards(user_id, cards)
        prepare_and_send_new_training_question(message.chat.id)
        return

    response = "TRAINING\nContinue training"
    BOT.reply_to(message, response, reply_markup=get_reply_keyboard_markup())



def prepare_and_send_new_training_question(user_id):
    cards = get_user_cached_cards(user_id)
    cards_count = len(cards)
    if cards_count < 4:
        response = f"TRAINING\nYou should add at least 4 cards.Now you have {cards_count}"
        BOT.send_message(user_id, response, reply_markup=get_reply_keyboard_markup())
        set_user_state(user_id, UserStates.MENU)
        return

    random_indexes = random.sample(range(0, cards_count), 4)
    question_index = random_indexes[random.randint(0, 3)]
    question = cards[question_index][0]
    valid_answer = cards[question_index][1]
    variants = []
    for i in random_indexes:
        variants.append(cards[i][1])

    response = "TRAINING\nWhat is the meaning for\n'" + question + "'"
    set_user_question(user_id, response)
    set_user_questuion_valid_answer(user_id, valid_answer)
    set_user_question_variants(user_id, variants)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(variants[0], callback_data=UserAnswerVariants.TRAINING_VARIANT_1),
                            types.InlineKeyboardButton(variants[1], callback_data=UserAnswerVariants.TRAINING_VARIANT_2),
                            types.InlineKeyboardButton(variants[2], callback_data=UserAnswerVariants.TRAINING_VARIANT_3),
                            types.InlineKeyboardButton(variants[3], callback_data=UserAnswerVariants.TRAINING_VARIANT_4))
    BOT.send_message(user_id, response, reply_markup=markup)
    set_user_state(user_id, UserStates.REQUEST_TRAINING)


@BOT.callback_query_handler(func=lambda call: True)
def training_answer_query_handler(call):
    user_id = get_user_id_by_message(call.message)
    if not is_user_exist(user_id):
        request_from_non_exits_user_processing(call.message)
        return
    if get_user_state(user_id) != UserStates.REQUEST_TRAINING:
        return

    correct_answer = get_user_questuion_valid_answer(user_id)
    if correct_answer is None:
        return
    question = get_user_question(user_id)
    if question is None:
        return

    # print(call.message.id)
    if call.message.text == question:
        answer_variant = call.data
        if answer_variant is None:
            return
    else:
        return
    user_answer = get_user_answer_variant(user_id, answer_variant)
    if user_answer is None:
        return

    if correct_answer == user_answer:
        response = f"TRAINING\nSuccess, you are right. Correct answer is\n{correct_answer}"
        BOT.send_message(user_id, response, reply_markup=get_reply_keyboard_markup())
        prepare_and_send_new_training_question(user_id)
        return

    response = f"TRAINING\nFail, try again, is not correct\n{user_answer}"
    BOT.send_message(call.message.chat.id, response, reply_markup=get_reply_keyboard_markup())
