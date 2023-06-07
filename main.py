from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles
from routers.route import router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    router=router,
    prefix=''
)


