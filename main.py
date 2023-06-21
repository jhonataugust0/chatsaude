import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.bot import Bot
from api.routes.register_user import RegisterUser
from api.routes.schedule_consult import ScheduleConsult
app = FastAPI()

origins = ["*"]

bot = Bot()
user = RegisterUser()
schedule_consult = ScheduleConsult()

app.include_router(bot.router)
app.include_router(user.router)
app.include_router(schedule_consult.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
