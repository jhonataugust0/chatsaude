from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.bot import Bot
import uvicorn
import logging

app = FastAPI()

origins = ["*"]

bot = Bot()

app.include_router(bot.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
#     logging.error(f"{request}: {exc_str}")
#     content = {"status_code": 10422, "message": exc_str, "data": None}
#     return JSONResponse(
#         content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
#     )


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
