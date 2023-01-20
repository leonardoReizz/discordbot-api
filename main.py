import uvicorn

from fastapi import FastAPI 
from database.connection import Settings
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user_router


app = FastAPI()
settings = Settings()

origins = [
  "*",
  "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(user_router, prefix="/user")


@app.on_event("startup")
async def init_db():
  await settings.initialize_database()

@app.get('/')
async def on():
  return { "message" : "ok" }

if __name__ == '__main__':
  uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)




# settings