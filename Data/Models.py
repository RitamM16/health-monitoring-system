from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Interval

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
   id: Mapped[int] = mapped_column(Integer, primary_key=True)
   email: Mapped[str] = mapped_column(String(200), primary_key=False)
   name: Mapped[str] = mapped_column(String(200), primary_key=False)

class Endpoint(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    url: Mapped[str] = mapped_column(String(200), primary_key=False)
    frequency: Mapped[int] = mapped_column(Integer, primary_key=False)
    method: Mapped[str] = mapped_column(String(200), primary_key=False)
    headers: Mapped[dict] = mapped_column(JSON, primary_key=False)
    success_criteria_status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    success_criteria_response_time: Mapped[int] = mapped_column(Integer, nullable=False)
    unhealthy_threshold_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_deleted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    
    
