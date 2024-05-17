from sqlmodel import Session, select
from . import models


class CustomNotFoundError(Exception):
    pass


def db_read_user_by_email(
    session: Session, user_basic: models.UserBasic
) -> models.UserInDB:
    user_in_db = session.exec(
        select(models.UserInDB).where(models.UserInDB.email == user_basic.email)
    ).first()
    if user_in_db is None:
        raise CustomNotFoundError("User not in DB")
    return user_in_db


def db_write_create_user(session: Session, db_user: models.UserInDB) -> models.UserInDB:
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def db_read_model_run_by_input(
    session: Session, model_input: models.ModelInput
) -> models.ModelRun:
    model_run = session.exec(
        select(models.ModelRun).where(
            models.ModelRun.model_input_text == model_input.text
        )
    ).first()
    if model_run is None:
        raise CustomNotFoundError("Model input not found in DB")
    return model_run


def db_write_model_run(session: Session, model_run: models.ModelRun) -> models.ModelRun:
    session.add(model_run)
    session.commit()
    session.refresh(model_run)
    return model_run


def db_read_openai_model_run_by_input(
    session: Session, openai_model_input: models.OpenAIModelInput
) -> models.OpenAIModelRun:
    openai_model_run = session.exec(
        select(models.OpenAIModelRun)
        .where(
            models.OpenAIModelRun.transplant_organ
            == openai_model_input.transplant_organ
        )
        .where(
            models.OpenAIModelRun.diagnosis_description
            == openai_model_input.diagnosis_description
        )
    ).first()
    if openai_model_run is None:
        raise CustomNotFoundError("Model input not found in DB")
    return openai_model_run


def db_write_openai_model_run(
    session: Session, openai_model_run: models.OpenAIModelRun
) -> models.OpenAIModelRun:
    session.add(openai_model_run)
    session.commit()
    session.refresh(openai_model_run)
    return openai_model_run


def db_read_all_openai_model_runs(
    session: Session,
):
    openai_model_runs = session.exec(select(models.OpenAIModelRun)).all()
    if openai_model_runs is None:
        return []
    else:
        return openai_model_runs


def db_read_all_model_runs(
    session: Session,
):
    model_runs = session.exec(select(models.ModelRun)).all()
    if model_runs is None:
        return []
    else:
        return model_runs
