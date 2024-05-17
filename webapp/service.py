from typing import Annotated
from sqlmodel import Session
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from transformers import pipeline
from . import db, crud
from .models import (
    UserInDB,
    UserBasic,
    UserInput,
    Token,
    ModelInput,
    ModelRun,
    OpenAIModelInput,
    OpenAIModelRun,
)

from openai import OpenAI
from dotenv import load_dotenv
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c8d1b2ccf7eadb75e96f54dc6d01721a2f65e89a402bf97ba29fee4d28790889"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

summarizer = pipeline("summarization", model="t5-small")

load_dotenv()
openai_client = OpenAI()


def create_user(session: Session, user_input: UserInput):
    hashed_password = pwd_context.hash(user_input.password)
    db_user = UserInDB(email=user_input.email, hashed_password=hashed_password)
    user_created = crud.db_write_create_user(session=session, db_user=db_user)
    return user_created


def register_user(session: Session, user_input: UserInput):
    try:
        user_basic = UserBasic(email=user_input.email)
        user_in_db = crud.db_read_user_by_email(session=session, user_basic=user_basic)
    except crud.CustomNotFoundError:
        user_created = create_user(session=session, user_input=user_input)
        return user_created
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")


def authenticate_user(
    session: Session, form_data_username: str, form_data_password: str
):
    try:
        user_basic = UserBasic(email=form_data_username)
        user_in_db = crud.db_read_user_by_email(session=session, user_basic=user_basic)
    except crud.CustomNotFoundError:
        return False
    if not pwd_context.verify(form_data_password, user_in_db.hashed_password):
        return False
    return user_in_db


def create_access_token(data: dict, expires_in_minutes: int | None = None) -> Token:
    if expires_in_minutes:
        access_expires_in_delta = timedelta(minutes=expires_in_minutes)
    else:
        access_expires_in_delta = timedelta(minutes=15)
    to_encode = data.copy()
    expire_in = datetime.now(timezone.utc) + access_expires_in_delta
    to_encode.update({"exp": expire_in})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    access_token = Token(access_token=encoded_jwt, token_type="bearer")
    return access_token


def authenticate_and_create_access_token(
    session: Session, form_data_username: str, form_data_password: str
):
    user_in_db = authenticate_user(
        session=session,
        form_data_username=form_data_username,
        form_data_password=form_data_password,
    )
    if not user_in_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user_in_db.email}, expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return access_token


def get_current_user(
    session: Annotated[Session, Depends(db.get_session)],
    token: Annotated[Token, Depends(oauth2_scheme)],
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_in_token: str = payload.get("sub")
        if username_in_token is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    try:
        user_basic = UserBasic(email=username_in_token)
        user_in_db = crud.db_read_user_by_email(session=session, user_basic=user_basic)
    except crud.CustomNotFoundError as exc:
        raise credentials_exception from exc

    return user_in_db


def read_or_create_model_run(
    session: Session, current_user: UserInDB, model_input: ModelInput
) -> ModelRun:
    try:
        model_run = crud.db_read_model_run_by_input(
            session=session, model_input=model_input
        )
    except crud.CustomNotFoundError:
        result = summarizer(model_input.text, max_length=100)
        model_run = ModelRun(
            email=current_user.email,
            model_input_text=model_input.text,
            model_output_text=result[0]["summary_text"],
        )
        model_run = crud.db_write_model_run(session=session, model_run=model_run)
    return model_run


def read_or_create_openai_model_run(
    session: Session,
    current_user: UserInDB,
    openai_model_input: OpenAIModelInput,
) -> OpenAIModelRun:

    try:
        openai_model_run = crud.db_read_openai_model_run_by_input(
            session=session, openai_model_input=openai_model_input
        )
    except crud.CustomNotFoundError:
        prompt_for_openai_call = openai_model_input.prompt_template.format(
            transplant_param=openai_model_input.transplant_organ,
            complication_param=openai_model_input.diagnosis_description,
        )
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant who gives output in JSON format.",
                },
                {"role": "user", "content": prompt_for_openai_call},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        response_message_content = completion.choices[0].message.content
        response_message_content_json = json.loads(response_message_content)
        json_keys = list(response_message_content_json.keys())
        classification = response_message_content_json[json_keys[0]]
        explanation = response_message_content_json[json_keys[1]]
        probability_within_90_days = response_message_content_json[json_keys[2]]
        openai_call_id = completion.id
        created = completion.created
        model = completion.model
        system_fingerprint = completion.system_fingerprint
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens

        openai_model_run = OpenAIModelRun(
            email=current_user.email,
            prompt_template=openai_model_input.prompt_template,
            transplant_organ=openai_model_input.transplant_organ,
            diagnosis_description=openai_model_input.diagnosis_description,
            classification=classification,
            explanation=explanation,
            probability_within_90_days=probability_within_90_days,
            openai_call_id=openai_call_id,
            created=created,
            model=model,
            system_fingerprint=system_fingerprint,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )
        openai_model_run = crud.db_write_openai_model_run(
            session=session, openai_model_run=openai_model_run
        )
    return openai_model_run


def read_all_openai_model_runs(
    session: Session,  # , current_user: models.UserInDB
) -> list[OpenAIModelRun]:
    openai_model_runs = crud.db_read_all_openai_model_runs(session=session)
    return openai_model_runs


def read_all_summarization_model_runs(
    session: Session,  # , current_user: models.UserInDB
) -> list[ModelRun]:
    model_runs = crud.db_read_all_model_runs(session=session)
    return model_runs
