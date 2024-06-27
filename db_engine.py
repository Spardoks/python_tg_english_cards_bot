from models import (
    User,
    UserCard,
    UserCardMeaning,
    create_engine,
    create_session_maker,
    create_tables
)

class DbEngine:
    def __init__(self, DSN, drop_all=False):
        self.DSN = DSN
        self.ENG = create_engine(self.DSN)
        create_tables(self.ENG, drop_all)
        self.SESSIONMAKER = create_session_maker(self.ENG)


    def is_user_id_exist(self, user_id):
        session = self.SESSIONMAKER()
        user = session.query(User).filter_by(id=user_id).first()
        return user is not None

    def is_user_chat_id_exist(self, chat_id):
        session = self.SESSIONMAKER()
        user = session.query(User).filter_by(chat_id=chat_id).first()
        return user is not None

    def is_user_card_name_exist(self, user_id, card_name):
        session = self.SESSIONMAKER()
        user_card = session.query(UserCard).filter_by(user_id=user_id, card_name=card_name).first()
        return user_card is not None


    # for debug
    def create_test_users(self):
        session = self.SESSIONMAKER()

        user1 = User(id=1, chat_id=11)
        user2 = User(id=2, chat_id=22)
        session.add(user1)
        session.add(user2)

        user1_words = [
            UserCard(id=1, user_id=user1.id, card_name="word1_1"),
            UserCard(id=2, user_id=user1.id, card_name="word2_1"),
            UserCard(id=3, user_id=user1.id, card_name="word3_1"),
        ]
        user2_words = [
            UserCard(id=4, user_id=user2.id, card_name="word1_2"),
            UserCard(id=5, user_id=user2.id, card_name="word2_2"),
            UserCard(id=6, user_id=user2.id, card_name="word3_3"),
        ]
        session.add_all(user1_words)
        session.add_all(user2_words)

        user1_meanings = [ UserCardMeaning(card_id=card.id, card_meaning=card.card_name + "_meaning11") for card in user1_words ]
        user2_meanings = [ UserCardMeaning(card_id=card.id, card_meaning=card.card_name + "_meaning22") for card in user2_words ]
        session.add_all(user1_meanings)
        session.add_all(user2_meanings)

        session.commit()

        return True

    def create_user_card(self, user_id, card_name, meaning):
        session = self.SESSIONMAKER()
        new_card_id = self.get_max_card_id() + 1
        user_card = UserCard(id=new_card_id, user_id=user_id, card_name=card_name)
        session.add(user_card)
        session.commit()

        meaning_id = self.get_max_meaning_id() + 1
        user_card_meaning = UserCardMeaning(id=meaning_id, card_id=new_card_id, card_meaning=meaning)
        session.add(user_card_meaning)
        session.commit()

        return new_card_id

    def create_user(self, user_id, chat_id):
        session = self.SESSIONMAKER()
        user = User(id=user_id, chat_id=chat_id)
        session.add(user)
        session.commit()

        return user_id


    def delete_user_card(self, user_id, card_name):
        session = self.SESSIONMAKER()
        card_id = self.get_user_card_id(user_id, card_name)
        self.delete_card_meaning(card_id)
        session.query(UserCard).filter_by(user_id=user_id, id=card_id).delete()
        session.commit()

        return card_id

    def delete_card_meaning(self, card_id):
        session = self.SESSIONMAKER()
        session.query(UserCardMeaning).filter_by(card_id=card_id).delete()
        session.commit()


    def get_max_user_id(self):
        session = self.SESSIONMAKER()
        max_user = session.query(User).order_by(User.id.desc()).first()
        if max_user is None:
            return 0
        return max_user.id

    def get_max_card_id(self):
        session = self.SESSIONMAKER()
        max_card = session.query(UserCard).order_by(UserCard.id.desc()).first()
        if max_card is None:
            return 0
        return max_card.id

    def get_max_meaning_id(self):
        session = self.SESSIONMAKER()
        max_meaning = session.query(UserCardMeaning).order_by(UserCardMeaning.id.desc()).first()
        if max_meaning is None:
            return 0
        return max_meaning.id


    def get_all_users(self):
        session = self.SESSIONMAKER()
        users = session.query(User).all()
        return users

    def get_user_cards_with_meanings(self, user_id):
        session = self.SESSIONMAKER()
        user_cards_with_meanings = session.query(UserCard, UserCardMeaning)\
            .join(UserCardMeaning, UserCard.id == UserCardMeaning.card_id)\
            .filter(UserCard.user_id == user_id).all()
        result = []
        for pair in user_cards_with_meanings:
            card_name = pair[0].card_name
            card_meaning = pair[1].card_meaning
            result.append((card_name, card_meaning))
        return result

    def get_card_meaning(self, card_id):
        session = self.SESSIONMAKER()
        user_card_meaning = session.query(UserCardMeaning).filter_by(card_id=card_id).first()
        return user_card_meaning

    def get_user_card_id(self, user_id, card_name):
        session = self.SESSIONMAKER()
        user_card = session.query(UserCard).filter_by(user_id=user_id, card_name=card_name).first()
        return user_card.id

    def get_user_card(self, user_id, card_id):
        session = self.SESSIONMAKER()
        user_card_name = session.query(UserCard).filter_by(user_id=user_id, id=card_id).first()
        return user_card_name

    def get_user_cards(self, user_id):
        session = self.SESSIONMAKER()
        user_cards = session.query(UserCard).filter_by(user_id=user_id).all()
        return user_cards

    def get_user_cards_count(self, user_id):
        session = self.SESSIONMAKER()
        user_cards_count = session.query(UserCard).filter_by(user_id=user_id).count()
        return user_cards_count

    def get_user_id_by_chat_id(self, chat_id):
        session = self.SESSIONMAKER()
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if user is None:
            return None
        return user.id
