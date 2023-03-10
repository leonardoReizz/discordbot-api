from typing import Optional
from beanie import init_beanie, PydanticObjectId
from pydantic import BaseModel, BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User

class Settings(BaseSettings):
  DATABASE_URL: Optional[str] = None
  SECRET_KEY: Optional[str] = None


  async def initialize_database(self):
    client = AsyncIOMotorClient(self.DATABASE_URL)
    await init_beanie(database = client.get_default_database(), document_models=[User])

  class Config:
    env_file=".env"



class Database:
  def __init__(self, model):
    self.model = model
    
  async def save(self, document):
    return await document.create()
    
  
  async def get(self, id: PydanticObjectId):
    doc = await self.model.get(id)

    if doc:
      return doc
    return False
  
  async def get_all(self):
    docs = await self.model.find_all().to_list()
    if docs:
      return docs
    return []
  
  async def update(self, id: PydanticObjectId, body: BaseModel):
    doc_id = id
    des_body = body.dict()

    des_body = {k: v for k, v in des_body.items() if v is not None}
    update_query = {"$set": {
      field: value for field, value in des_body.items()
    }}

    doc = await self.get(doc_id)
    if not doc:
      return False

    await doc.update(update_query)
    return doc
  
  async def delete(self, id: PydanticObjectId):
    doc = await self.get(id)
    if not doc:
      return False
  
    await doc.delete()
    return True