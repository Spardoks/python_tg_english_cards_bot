# from models import *


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


def is_user_exist(user_id):
    return user_id in KNOWN_USERS and get_user_state(user_id) != UserStates.NOT_CREATED



def init_users():
    # TODOadd from db
    return True


def create_user(user_id):
    # TODOadd to db
    try:
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
        KNOWN_USERS[user_id][UserFields.CARDS] = {
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
    except KeyError:
        return False

    return True


def get_user_cards_with_meanings(user_id):
    # TODOget from db
    cards = {} if len(KNOWN_USERS[user_id][UserFields.CARDS]) == 0 else []
    try:
        for card, meaning in KNOWN_USERS[user_id][UserFields.CARDS].items():
            cards.append((card, meaning))
    except KeyError:
        return None
    return cards


def get_user_card_meaning(user_id, card):
    # TODOget from db
    try:
        return KNOWN_USERS[user_id][UserFields.CARDS][card]
    except KeyError:
        return None


def is_user_card_exist(user_id, card):
    # TODOget from db
    try:
        return card in KNOWN_USERS[user_id][UserFields.CARDS]
    except KeyError:
        return None


def create_user_card(user_id, card, meaning):
    # TODOadd to db
    # TODOadd if aleady not exist
    try:
        KNOWN_USERS[user_id][UserFields.CARDS][card] = meaning
    except KeyError:
        return False, 0
    return True, len(KNOWN_USERS[user_id][UserFields.CARDS])


def delete_user_card(user_id, card):
    # TODOdelete from db
    try:
        del KNOWN_USERS[user_id][UserFields.CARDS][card]
    except KeyError:
        return None
    return card not in KNOWN_USERS[user_id][UserFields.CARDS]
