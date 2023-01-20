import datetime
import time

from fastapi import APIRouter
from models.user import User
from fastapi import HTTPException, status
from database.connection import Database



user_router = APIRouter(tags=["user"])
user_database = Database(User)

@user_router.post('/register')
async def create_user(user: User):
  user_exist = await User.find_one(User.memberID == user.memberID)

  if user_exist:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="memberID already exists"
    )
  
  date = datetime.date.today()
  unixDate = time.mktime(date.timetuple())

  user.createdAt = unixDate
  user.updatedAt = unixDate
  
  createUser = await user_database.save(user)

  return {
    "message": createUser
  }

