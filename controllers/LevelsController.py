from routers.models import LevelsModels
from database.models import DefaultLevel
from sqlalchemy import insert, func, update
from database.engine import get_local_session
from fastapi import status
from fastapi.encoders import jsonable_encoder
import json


def levelExists(level):
    try:
        session = get_local_session()
        queried = session.query(DefaultLevel).filter(func.lower(DefaultLevel.level_name) == func.lower(level.title))
        exists = session.query(queried.exists()).scalar()
        session.close()
        return exists
    except Exception as e:
        raise Exception(str(e))
    

def levelIdExists(levelId):
    try:
        session = get_local_session()
        queried = session.query(DefaultLevel).filter(DefaultLevel.id == levelId)
        exists = session.query(queried.exists()).scalar()
        session.close()
        return exists
    except Exception as e:
        raise Exception(str(e))


def createLevel(level):
    if not levelExists(level):
        if len(level.initial_position) != 2:
            raise Exception("La posicion inicial debe contener 2 elementos: Posicion en X, y posición en Z.")
        session = get_local_session()
        statement = insert(DefaultLevel).values(
            level_name = level.title,
            level_json = json.dumps(jsonable_encoder(level)),
            x_init_car = level.initial_position[0],
            y_initial_car = 3,
            z_initial_car = level.initial_position[1]
        )
        try:
            session.execute(statement)
            session.commit()
            session.close()
            return "El nivel "+level.title+" ha sido creado exitosamente."
        except Exception as e:
            raise Exception(str(e))
    else:
        raise Exception("Ya existe un nivel con el título enviado.")
    

def deleteLevel(levelId):
    try:
        session = get_local_session()
        if not levelIdExists(levelId):
            raise Exception("No existe un nivel con el id "+str(levelId)+".")
        queried = session.query(DefaultLevel).filter(DefaultLevel.id == levelId).delete()
        session.commit()
        session.close()
        return "El nivel con id "+str(levelId)+" ha sido eliminado exitosamente."
    except Exception as e:
        raise Exception(str(e))
    

def updateLevel(levelId, level):
    try:
        session = get_local_session()
        if not levelIdExists(levelId):
            raise Exception("No existe un nivel con el id "+str(levelId)+".")
        if len(level.initial_position) != 2:
            raise Exception("La posicion inicial debe contener 2 elementos: Posicion en X, y posición en Z.")
        statement = update(DefaultLevel).where(DefaultLevel.id == levelId).values(
            level_name = level.title,
            level_json = json.dumps(jsonable_encoder(level)),
            x_initial_car = level.initial_position[0],
            y_initial_car = 3,
            z_initial_car = level.initial_position[1]
        )
        session.execute(statement)
        session.commit()
        session.close()
        return "El nivel con id "+str(levelId)+" ha sido modificado exitosamente."
    except Exception as e:
        raise Exception(str(e))

def getlevels():
    try:
        session = get_local_session()
        queried = session.query(DefaultLevel).all()
        session.close()
        return queried
    except Exception as e:
        raise Exception(str(e))



