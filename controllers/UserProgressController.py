from database.models import UserLevelFinished, User
from sqlalchemy import insert, update
from database.engine import get_local_session
from controllers.LevelsController import levelIdExists

def user_exists_with_id(id):
    try:
        session = get_local_session()
        queried = session.query(User).filter(User.id == id)
        exists = session.query(queried.exists()).scalar()
        session.close()
        return exists
    except Exception as e:
        raise Exception(str(e))
    

def userProgressExists(userId, levelId):
    try:
        session = get_local_session()
        queried = session.query(UserLevelFinished).filter(
            UserLevelFinished.user_id == userId).filter(
            UserLevelFinished.default_level_id == levelId)
        exists = session.query(queried.exists()).scalar()
        session.close()
        return exists
    except Exception as e:
        raise Exception(str(e))


def isHigherNewScore(score, time, userId, levelId):
    try:
        session = get_local_session()
        queried = session.query(UserLevelFinished).filter(
            UserLevelFinished.user_id == userId).filter(
            UserLevelFinished.default_level_id == levelId)
        data = queried.first()
        return (data.best_score < score or (data.best_score == score and time < data.best_time))
    except Exception as e:
        raise Exception(str(e))


def updateLevelProgress(score, time, user_id, level_id):
    try:
        session = get_local_session()
        statement = update(UserLevelFinished).where(
            UserLevelFinished.user_id == user_id
            and
            UserLevelFinished.default_level_id == level_id
        ).values(
            best_score = score,
            best_time = time
        )
        session.execute(statement)
        session.commit()
        session.close()
    except Exception as e:
        raise Exception(str(e))


def insertLevelProgress(score, time, user_id, level_id):
    try:
        session = get_local_session()
        statement = insert(UserLevelFinished).values(
            user_id = user_id,
            default_level_id = level_id,
            best_score = score,
            best_time = time
        )
        session.execute(statement)
        session.commit()
        session.close()
    except Exception as e:
        raise Exception(str(e))


def submitLevelProgress(score, time, user_id, level_id):
    if not user_exists_with_id(user_id):
        raise Exception("El usuario con el id indicado no existe.")
    if not levelIdExists(level_id):
        raise Exception("El nivel con el id indicado no existe.")
    exists = userProgressExists(user_id, level_id)
    if exists and isHigherNewScore(score, time, user_id, level_id):
        updateLevelProgress(score, time, user_id, level_id)
        return "El progreso del usuario en el nivel ha sido actualizado exitosamente."
    elif not exists:
        insertLevelProgress(score, time, user_id, level_id)
        return "El progreso del usuario en el nivel ha sido generado exitosamente."
    else:
        return "El nuevo puntaje no ha superado el mejor puntaje del usuario."
    

def retrieveLevelProgress(user_id, level_id):
    try:
        session = get_local_session()
        queried = session.query(UserLevelFinished).filter(
            UserLevelFinished.user_id == user_id).filter(
            UserLevelFinished.default_level_id == level_id)
        progressData = queried.first()
        session.close()
        return {
            "completed": True,
            "best_time": progressData.best_time,
            "best_score": progressData.best_score
        }
    except Exception as e:
        raise Exception(str(e))


def getLevelProgress(user_id, level_id):
    if not user_exists_with_id(user_id):
        raise Exception("El usuario con el id indicado no existe.")
    if not levelIdExists(level_id):
        raise Exception("El nivel con el id indicado no existe.")
    if not userProgressExists(user_id, level_id):
        return {
            "completed": False,
            "best_time": None,
            "best_score": None
        }
    else:
        return retrieveLevelProgress(user_id, level_id)
