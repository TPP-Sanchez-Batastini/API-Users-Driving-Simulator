from pydantic import BaseModel

class EndOfLevel(BaseModel):
    score: float
    time: float #Milliseconds
    levelId: int
    userId: int


class ProgressData(BaseModel):
    levelId: int
    userId: int