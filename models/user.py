from beanie import Document
from pydantic import BaseModel

class User(Document):
  memberID: str
  entryDate: int
  exitDate: int 
  createdAt: int | None
  updatedAt: int | None

  class Settings:
    user = "user"

  class Config:
    schema_extra =  {
      "example": {
        "userDiscordID": '282859044593598464',
        "entryDate": 1674121735,
        "exitDate": 1674126735,
      }
    }
