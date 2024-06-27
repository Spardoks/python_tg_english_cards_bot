from models import *
from config import DSN
from db_engine import DbEngine


DB_ENGINE = DbEngine(DSN, drop_all=False)

KNOWN_USERS = {}


class UserFields:
    STATE = 'state'
    CARDS = 'cards'
    NEW_CARD_REQUEST = 'new_card'
    DELETE_CARD_REQUEST = 'delete_card'
    TRAINING_CARD = 'training_card'
    TRAINING_CARD_MEANING = 'training_card_meaning'
    TRAINING_CARD_VARIANTS = 'training_card_variants'
    TMP_DICT = 'all_cards_cahced'

class UserStates:
    NOT_CREATED = -1
    MENU = 0
    REQUEST_NEW_CARD = 1
    REQUEST_NEW_CARD_MEANING = 2
    REQUEST_DELETE_CARD = 3
    REQUEST_DELETE_CARD_CONFIRM = 4
    REQUEST_TRAINING = 5

class UserAnswerVariants:
    TRAINING_VARIANT_1 = "cb_training_1"
    TRAINING_VARIANT_2 = "cb_training_2"
    TRAINING_VARIANT_3 = "cb_training_3"
    TRAINING_VARIANT_4 = "cb_training_4"
    CONFIRM_DELETE = "YES"


####################### WORKING WITH CACHED DATA #######################

def set_user_state(user_id, state):
    KNOWN_USERS[user_id][UserFields.STATE] = state

def set_user_add_card(user_id, card):
    KNOWN_USERS[user_id][UserFields.NEW_CARD_REQUEST] = card

def set_user_delete_card(user_id, card):
    KNOWN_USERS[user_id][UserFields.DELETE_CARD_REQUEST] = card

def set_user_cached_cards(user_id, cards):
    KNOWN_USERS[user_id][UserFields.TMP_DICT] = cards

def set_user_question(user_id, question):
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD] = question

def set_user_questuion_valid_answer(user_id, answer):
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_MEANING] = answer

def set_user_question_variants(user_id, variants):
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS] = {}
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS][UserAnswerVariants.TRAINING_VARIANT_1] = variants[0]
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS][UserAnswerVariants.TRAINING_VARIANT_2] = variants[1]
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS][UserAnswerVariants.TRAINING_VARIANT_3] = variants[2]
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS][UserAnswerVariants.TRAINING_VARIANT_4] = variants[3]


def get_user_add_card(user_id):
    return KNOWN_USERS[user_id].get(UserFields.NEW_CARD_REQUEST, None)

def get_user_delete_card(user_id):
    return KNOWN_USERS[user_id].get(UserFields.DELETE_CARD_REQUEST, None)

def get_user_state(user_id):
    return KNOWN_USERS[user_id].get(UserFields.STATE, None)

def get_user_cached_cards(user_id):
    return KNOWN_USERS[user_id].get(UserFields.TMP_DICT, None)

def get_user_id_by_message(message):
    return message.chat.id

def get_user_question(user_id):
    return KNOWN_USERS[user_id].get(UserFields.TRAINING_CARD, None)

def get_user_questuion_valid_answer(user_id):
    return KNOWN_USERS[user_id].get(UserFields.TRAINING_CARD_MEANING, None)

def get_user_answer_variant(user_id, variant_index):
    return KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS].get(variant_index, None)


####################### WORKING WITH DB #######################

def init_users():
    # return tests_db_users()
    # tests_db_users()
    try:
        users = DB_ENGINE.get_all_users()
        for user in users:
            chat_id = user.chat_id
            KNOWN_USERS[chat_id] = {}
            KNOWN_USERS[chat_id][UserFields.STATE] = UserStates.MENU
            KNOWN_USERS[chat_id][UserFields.NEW_CARD_REQUEST] = ""
            KNOWN_USERS[chat_id][UserFields.DELETE_CARD_REQUEST] = ""
            KNOWN_USERS[chat_id][UserFields.TRAINING_CARD] = ""
            KNOWN_USERS[chat_id][UserFields.TRAINING_CARD_MEANING] = ""
            KNOWN_USERS[chat_id][UserFields.TRAINING_CARD_VARIANTS] = {
                UserAnswerVariants.TRAINING_VARIANT_1: "",
                UserAnswerVariants.TRAINING_VARIANT_2: "",
                UserAnswerVariants.TRAINING_VARIANT_3: "",
                UserAnswerVariants.TRAINING_VARIANT_4: ""
            }
    except Exception as e:
        print("Error while init users", e)
        return False
    return True


def is_user_exist(user_id):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        return user_db_id is not None and get_user_state(user_id) != UserStates.NOT_CREATED
    except Exception as e:
        print("Error while checking user in db", e)
        return False


def create_user(user_id):
    try:
        prepare_cards = {
            "word1": "meaning1",
            "word2": "meaning2",
            "word3": "meaning3",
            "word4": "meaning4",
            "word5": "meaning5",
            "word6": "meaning6",
            "word7": "meaning7",
            "word8": "meaning8",
            "word9": "meaning9",
            "word10": "meaning10"
        }
        user_db_id = DB_ENGINE.get_max_user_id() + 1
        result = DB_ENGINE.create_user(user_id=user_db_id, chat_id=user_id)
        if result != user_db_id:
            return False
        for key, value in prepare_cards.items():
            DB_ENGINE.create_user_card(user_db_id, key, value)
    except Exception as e:
        print("Error create_user", e)
        return False
    KNOWN_USERS[user_id] = {}
    KNOWN_USERS[user_id][UserFields.STATE] = UserStates.MENU
    KNOWN_USERS[user_id][UserFields.TMP_DICT] = {}
    KNOWN_USERS[user_id][UserFields.NEW_CARD_REQUEST] = ""
    KNOWN_USERS[user_id][UserFields.DELETE_CARD_REQUEST] = ""
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD] = ""
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_MEANING] = ""
    KNOWN_USERS[user_id][UserFields.TRAINING_CARD_VARIANTS] = {
        UserAnswerVariants.TRAINING_VARIANT_1: "",
        UserAnswerVariants.TRAINING_VARIANT_2: "",
        UserAnswerVariants.TRAINING_VARIANT_3: "",
        UserAnswerVariants.TRAINING_VARIANT_4: ""
    }
    return True


def get_user_cards_with_meanings(user_id):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        cards = DB_ENGINE.get_user_cards_with_meanings(user_db_id)
        return cards
    except Exception as e:
        print("Error get_user_cards_with_meanings", e)
        return None


def get_user_card_meaning(user_id, card):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        card_id = DB_ENGINE.get_user_card_id(user_db_id, card)
        return DB_ENGINE.get_card_meaning(card_id).card_meaning
    except Exception as e:
        print("Error get_user_card_meaning", e)
        return None


def is_user_card_exist(user_id, card):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        return DB_ENGINE.is_user_card_name_exist(user_db_id, card)
    except Exception as e:
        print("Error is_user_card_exist", e)
        return None


def create_user_card(user_id, card, meaning):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        DB_ENGINE.create_user_card(user_db_id, card, meaning)
        cards_count = DB_ENGINE.get_user_cards_count(user_db_id)
    except Exception as e:
        print("Error create_user_card", e)
        return False, 0
    return True, cards_count


def delete_user_card(user_id, card):
    try:
        user_db_id = DB_ENGINE.get_user_id_by_chat_id(user_id)
        card_id = DB_ENGINE.delete_user_card(user_db_id, card)
        return card_id is not None
    except Exception as e:
        print("Error delete_user_card", e)
        return None



# for debug
def tests_db_users():
    print("empty_db")
    db_users_telegram_ids = DB_ENGINE.get_all_users()
    print(db_users_telegram_ids)
    print()

    print("test_db")
    DB_ENGINE.create_test_users()
    db_users = DB_ENGINE.get_all_users()
    print(db_users_telegram_ids)
    for user in db_users:
        print(user)

        user_cards = DB_ENGINE.get_user_cards(user.id)
        print(user_cards)

        for user_card in user_cards:
            print(user_card)
            user_card_meaning = DB_ENGINE.get_card_meaning(user_card.id)
            print(user_card_meaning)
            print()


        user_cards_with_meanings = DB_ENGINE.get_user_cards_with_meanings(user.id)
        print(user_cards_with_meanings)

        print('\n')

    print("--------------------------------------")
    print(DB_ENGINE.is_user_chat_id_exist(333))
    new_user_id = DB_ENGINE.get_max_user_id() + 1
    print(DB_ENGINE.is_user_id_exist(new_user_id))
    DB_ENGINE.create_user(new_user_id, 333)
    print(DB_ENGINE.is_user_id_exist(new_user_id))
    print(DB_ENGINE.is_user_chat_id_exist(333))
    print(DB_ENGINE.is_user_card_name_exist(new_user_id, "test"))
    card_id = DB_ENGINE.create_user_card(new_user_id, "test", "meaning of test")
    print(DB_ENGINE.is_user_card_name_exist(new_user_id, "test"))
    meaning = DB_ENGINE.get_card_meaning(card_id)
    print(meaning)
    DB_ENGINE.delete_user_card(new_user_id, "test")
    print(DB_ENGINE.is_user_card_name_exist(new_user_id, "test"))

    return False
