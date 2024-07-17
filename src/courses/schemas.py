from pydantic import BaseModel

from typing import Union


class NewClass(BaseModel):
    title: str
    video_link: str
    description: str
    previous_id: Union[int, None] = None
    next_id: Union[int, None] = None
    module_id: int
