from pydantic import BaseModel
from typing import Optional, List

class Street(BaseModel):
    position_x: float
    position_y: float
    rotation: float
    long_x: int
    long_y: int
    type: str

class ThreeDObjects(BaseModel):
    position_x: float
    position_y: float
    rotation: float
    type: str


class Checkpoint(BaseModel):
    position_x: float
    position_y: float
    end: bool

class LevelJSON(BaseModel):
    streets: List[Street]
    objects: Optional[List[ThreeDObjects]]
    checkpoints: Optional[List[Checkpoint]]
    minimum_to_win: Optional[float]
    has_traffic: bool
    initial_position: List[float]
    initial_rotation: float
    description: str
    title: str
    image: str


