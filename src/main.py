import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.gateway.routes.bot import Bot
from src.gateway.routes.register_user import RegisterUser
from src.gateway.routes.schedule_consult import ScheduleConsult
from src.gateway.routes.schedule_exam import ScheduleExam
app = FastAPI()

origins = ["*"]

bot = Bot()
user = RegisterUser()
schedule_consult = ScheduleConsult()
exam_consult = ScheduleExam()

app.include_router(bot.router)
app.include_router(user.router)
app.include_router(schedule_consult.router)
app.include_router(exam_consult.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=2) #,
