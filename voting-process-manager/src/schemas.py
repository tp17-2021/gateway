from pydantic import BaseModel
from typing import List

class Member(BaseModel):
    name: str
    agree: bool

class CommissionPaper(BaseModel):
    polling_place_id: int
    participated_members: List[Member] = None
    president: Member
    class Config:
        schema_extra = {
            "example": {
                "polling_place_id": 0,
                "participated_members": [
                    {
                        "name": "Bc. Libor Duda",
                        "agree": True
                    },
                    {
                        "name": "Bc. Timotej Králik",
                        "agree": False
                    },
                    {
                        "name": "Bc. Lucia Janíková",
                        "agree": True
                    }
                ],
                "president": {
                    "name": "Boris Osuský",
                    "agree": True
                }
            }
        }