from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, JSON, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class ApppUserModel(Base):
    __tablename__ = "appusers"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    



class ChatModel(Base):
    __tablename__ = "chat"
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("appusers.user_id"), nullable=False)
    #db_credentials = Column(JSON) las credenciales de la base de datos `edubot` estarán quemadas en el .env
    chat_model_provider = Column(JSON) # Aquí espero un json, por ejemplo: {"client":google, "model":"gemini-2.0-flash", "temperature":0.2} por ahora "model" seran los disponibles por google, groq y deepseek

    user = relationship("UserModel", backref="chats")



class MessageModel(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("appusers.user_id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.chat_id"), nullable=False)

    role = Column(String)
    message = Column(JSON)
    date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", backref="message")
    chat = relationship("ChatModel", backref="message")

