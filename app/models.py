

from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class DetectionHistory(Base):
    __tablename__ = "detection_history"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    bbox = Column(JSON, nullable=False)


# # Post table
# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, nullable=False)
#     content = Column(String, nullable=False)
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

#     # Back reference to User
#     owner = relationship("User", back_populates="posts")
# ```

