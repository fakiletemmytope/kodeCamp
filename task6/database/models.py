from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.db_connect import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    # blogs = relationship("Item", back_populates="owner")
    
    

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    author_name = Column(String, index=True)
    author_id = Column(Integer, index= True)
    
    
Base.metadata.create_all(bind=engine)