from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import engine, Base




class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    users = relationship("User", back_populates="role")


class UserClass(Base):
    __tablename__ = "user_classes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], overlaps="classes")
    class_ = relationship("Class", foreign_keys=[class_id], overlaps="users")


class UserCourse(Base):
    __tablename__ = "user_courses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User", foreign_keys=[user_id], overlaps="courses")
    course = relationship("Course", foreign_keys=[course_id], overlaps="users")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    courses = relationship(
        "Course", secondary="user_courses", back_populates="users")
    classes = relationship(
        "Class", secondary="user_classes", back_populates="users")
    
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")




class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    users = relationship("User", secondary="user_courses",
                         back_populates="courses")
    modules = relationship("Module", back_populates="course")
    events = relationship("Event", back_populates="course")


class Module(Base):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    previous_id = Column(Integer)
    next_id = Column(Integer)
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", back_populates="modules")
    classes = relationship("Class", back_populates="module")
    created_at = Column(DateTime, server_default=func.now())


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    video_link = Column(String(255))
    description = Column(Text)
    previous_id = Column(Integer)
    next_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    module_id = Column(Integer, ForeignKey("module.id"))
    module = relationship("Module", back_populates="classes")
    users = relationship("User", secondary="user_classes",
                         back_populates="classes")


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    event_date = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=False)
    event_link = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", back_populates="events")


Base.metadata.create_all(bind=engine)
