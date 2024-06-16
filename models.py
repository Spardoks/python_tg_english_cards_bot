import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    chat_id = sq.Column(sq.Integer)

    def __str__(self):
        return str(self.chat_id)

class UserCard(Base):
    __tablename__ = "cards"

    id = sq.Column(sq.Integer, primary_key=True)
    card = sq.Column(sq.String)
    meaning = sq.Column(sq.String)

    def __str__(self):
        return f"{self.id}: {self.word} - {self.translation}"

class UserMeaning(Base):
    __tablename__ = "meanings"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    card_id = sq.Column(sq.Integer, sq.ForeignKey("cards.id"))
    meaning = sq.Column(sq.String)

    user = relationship(User, backref="users")
    word = relationship(UserCard, backref="cards")

    def __str__(self):
        return f"{self.id}: {self.user_id} - {self.word_id}"



def add_user(session, user_id):
    pass

def add_card(session, user_id, card):
    pass

def add_card_meaning(session, card_id, meaning):
    pass

def get_cards(session, user_id):
    pass


def create_engine(DSN):
    return sq.create_engine(DSN)

def create_session_maker(engine):
    return sessionmaker(bind=engine)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)