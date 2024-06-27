import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    chat_id = sq.Column(sq.Integer)

    def __str__(self):
        return f"User: id = {self.id}, chat_id = {self.chat_id}"

class UserCard(Base):
    __tablename__ = "cards"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    card_name = sq.Column(sq.String)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="cards")

    def __str__(self):
        return f"UserCard: id = {self.id}, key = {self.card_name}, user_id = {self.user_id}"

class UserCardMeaning(Base):
    __tablename__ = "meanings"

    id = sq.Column(sq.Integer, primary_key=True)
    card_meaning = sq.Column(sq.String)
    card_id = sq.Column(sq.Integer, sq.ForeignKey("cards.id"), nullable=False)

    card = relationship("UserCard", backref="meanings")

    def __str__(self):
        return f"UserCardMeaning: id = {self.id}, meaning = {self.card_meaning}, card_id = {self.card_id}"



def create_engine(DSN):
    return sq.create_engine(DSN)

def create_session_maker(engine):
    return sessionmaker(bind=engine)

def create_tables(engine, drop_all=False):
    if drop_all:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
