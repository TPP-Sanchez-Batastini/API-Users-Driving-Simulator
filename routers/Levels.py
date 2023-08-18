from fastapi import APIRouter, status, HTTPException
from routers.models import LevelsModels
from controllers import LevelsController

router = APIRouter()

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_level(level: LevelsModels.LevelJSON):
    try:
        response = LevelsController.createLevel(level)
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500, 
            detail= str(e)
        )
    
@router.get("/", status_code = status.HTTP_200_OK)
def get_levels():
    try:
        response = LevelsController.getlevels()
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
    

@router.delete("/", status_code = status.HTTP_200_OK)
def delete_level(levelId: int):
    try:
        response = LevelsController.deleteLevel(levelId)
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
    


@router.put("/", status_code = status.HTTP_200_OK)
def update_level(levelId: int, level: LevelsModels.LevelJSON):
    try:
        response = LevelsController.updateLevel(levelId, level)
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )