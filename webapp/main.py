from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import Session
from . import db, models, service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_session_dependency = Annotated[Session, Depends(db.get_session)]
current_user_dependency = Annotated[models.UserInDB, Depends(service.get_current_user)]


@app.get("/")
def home():
    return "Hello World"


@app.post("/register", response_model=models.UserInDB)
async def register(session: db_session_dependency, user_input: models.UserInput):
    user_created = service.register_user(session=session, user_input=user_input)
    return user_created


@app.post("/token", response_model=models.Token)
async def login_for_token(
    session: db_session_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    access_token = service.authenticate_and_create_access_token(
        session=session,
        form_data_username=form_data.username,
        form_data_password=form_data.password,
    )
    return access_token


@app.post("/summarize", response_model=models.ModelRun)
async def summarize(
    session: db_session_dependency,
    current_user: current_user_dependency,
    current_model_input: models.ModelInput,
):
    model_run = service.read_or_create_model_run(
        session=session, current_user=current_user, model_input=current_model_input
    )
    return model_run


@app.post("/transplantdiagrelation", response_model=models.OpenAIModelRun)
async def openai_chat_completion(
    session: db_session_dependency,
    current_user: current_user_dependency,
    openai_model_input: models.OpenAIModelInput,
):
    openai_model_run = service.read_or_create_openai_model_run(
        session=session,
        current_user=current_user,
        openai_model_input=openai_model_input,
    )
    return openai_model_run


@app.get("/openaimodelruns", response_model=list[models.OpenAIModelRun])
async def openai_all_model_runs(
    session: db_session_dependency,  # , current_user: current_user_dependency,
):
    openai_model_runs = service.read_all_openai_model_runs(
        session=session  # , current_user=current_user
    )
    return openai_model_runs


@app.get("/summarizemodelruns", response_model=list[models.ModelRun])
async def summarize_all_model_runs(
    session: db_session_dependency,  # , current_user: current_user_dependency,
):
    model_runs = service.read_all_summarization_model_runs(
        session=session  # , current_user=current_user
    )
    return model_runs
