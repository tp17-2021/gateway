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
                        "name": "Jožko Mrkvička",
                        "agree": True
                    },
                    {
                        "name": "Ferko Mrkvička",
                        "agree": False
                    },
                    {
                        "name": "Ján Mrkvička",
                        "agree": True
                    }
                ],
                "president": {
                    "name": "Jožko Hlavný",
                    "agree": True
                }
            }
        }