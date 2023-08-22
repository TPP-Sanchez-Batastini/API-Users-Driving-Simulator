
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, UniqueConstraint, Time, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # Might have password or it is federated. But never both of them
        # Or you use password with normal login, or you login with federated account
        # But email can only be used once...
        CheckConstraint('NOT(password IS NULL AND federated_with IS NULL)'),
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("user_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    password = Column("password", String(10000))
    federated_with = Column("federated_with", String(200))


class DefaultLevel(Base):
    __tablename__ = "default_levels"

    id = Column("default_level_id", Integer, primary_key=True, autoincrement = True)
    level_name = Column("level_name", String(255), nullable = False)
    level_json = Column("level_json", String(65535), nullable = False)
    x_initial_car = Column("x_init_car", Float, nullable = False)
    y_initial_car = Column("y_initial_car", Float, nullable = False)
    z_initial_car = Column("z_initial_car", Float, nullable = False)


class CustomLevel(Base):
    __tablename__ = "custom_levels"
    __table_args__ = (
        UniqueConstraint('level_name', 'author_id', 'date_created', 'level_json'),
    )

    id = Column("custom_level_id", Integer, primary_key=True, autoincrement = True)
    level_name = Column("level_name", String(255), nullable = False)
    author_id = Column("author_id", Integer, ForeignKey("users.id"), nullable = False)
    date_created = Column("date_created", Date, nullable = False)
    level_json = Column("level_json", String(65535), nullable = False)
    x_initial_car = Column("x_init_car", Float, nullable = False)
    y_initial_car = Column("y_initial_car", Float, nullable = False)
    z_initial_car = Column("z_initial_car", Float, nullable = False)


class UserLevelFinished(Base):
    __tablename__ = "user_levels_finished"
    __table_args__ = (
        CheckConstraint('NOT(custom_level_id IS NULL AND default_level_id IS NULL)'),
        CheckConstraint('NOT(user_id IS NULL)'),
    )
    id = Column("finished_id", Integer, primary_key=True, autoincrement = True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    custom_level_id = Column("custom_level_id", Integer, ForeignKey("custom_levels.custom_level_id"))
    default_level_id = Column("default_level_id", Integer, ForeignKey("default_levels.default_level_id"))
    best_score = Column("best_score", Float, nullable = False)
    best_time = Column("best_time", Float, nullable = False)


class LevelTag(Base):
    __tablename__ = "levels_tags"
    __table_args__ = (
        CheckConstraint('NOT(custom_level_id IS NULL AND default_level_id IS NULL)'),
    )

    custom_level_id = Column("custom_level_id", Integer, ForeignKey("custom_levels.custom_level_id"), primary_key=True)
    default_level_id = Column("default_level_id", Integer, ForeignKey("default_levels.default_level_id"), primary_key=True)
    tag = Column("tag", String(100), primary_key = True)
