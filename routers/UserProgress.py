from fastapi import APIRouter, status, HTTPException
from routers.models.ProgressModels import EndOfLevel
from controllers.UserProgressController import submitLevelProgress, getLevelProgress

router = APIRouter()

@router.post("/end_of_level", status_code = status.HTTP_200_OK)
def submit_end_of_level(endOfLevelData: EndOfLevel):
    try:
        submitRes = submitLevelProgress(endOfLevelData.score, endOfLevelData.time, endOfLevelData.userId, endOfLevelData.levelId)
        return submitRes
    except Exception as e:
        raise HTTPException(
            status_code = 500, 
            detail= str(e)
        )
    

@router.get("/", status_code = status.HTTP_200_OK)
def get_progress_data(level_id: int, user_id: int):
    try:
        print(level_id)
        submitRes = getLevelProgress(user_id, level_id)
        return submitRes
    except Exception as e:
        raise HTTPException(
            status_code = 500, 
            detail= str(e)
        )