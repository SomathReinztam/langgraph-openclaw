from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import contextmanager
from typing import Dict, Optional, List, Any
from datetime import datetime
from src.database import models
from src.utils import settings


from src.database.schemas import DatabaseError

class CrudHelper:
    def __init__(self):
        self.conn_string = f"postgresql+psycopg2://{settings.APP_DB_USER}:{settings.APP_DB_PASS}@{settings.APP_DB_HOST}:{settings.APP_DB_PORT}/{settings.APP_DB_NAME}"
        self.engine = create_engine(self.conn_string)
    
    @contextmanager
    def session_scope(self):
        """
        Context manager para manejar sesiones de base de datos de forma segura
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f"Error en base de datos: {str(e)}") from e
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()


    def create_database(self) -> None:
        """
        Crea todas las tablas en la base de datos
        """
        try:
            models.Base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            raise DatabaseError(f"No se pudo crear la base de datos: {str(e)}") from e
    


    def new_user(self, name : str, email : str, password : str):
                with self.session_scope() as session:
                    user_db = models.ApppUserModel(
                    name=name,
                    email=email,
                    password=password
                )
                
                session.add(user_db)
                session.flush()
    

    def new_chat(self, user_id : str, chat_model_provider : Dict[str, Any]):
         
        with self.session_scope() as session:
            chat_db = models.ChatModel(
                user_id=user_id,
                chat_model_provider=chat_model_provider
            )

            session.add(chat_db)
            session.flush()
    
    

            