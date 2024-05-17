from sqlmodel import SQLModel, Field
from typing import Union


class UserBasic(SQLModel):
    email: str = Field(default=None)


class UserInput(UserBasic):
    password: str = Field(default=None)


class UserInDB(UserBasic, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)


class Token(SQLModel):
    access_token: str
    token_type: str


class ModelInput(SQLModel):
    text: str


class ModelOutput(SQLModel):
    text: str


class ModelRun(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: Union[str, None] = Field(default=None)
    model_input_text: Union[str, None] = Field(default=None)
    model_output_text: Union[str, None] = Field(default=None)


class OpenAIModelInput(SQLModel):
    prompt_template: str = Field(default=None)
    transplant_organ: str = Field(default=None)
    diagnosis_description: str = Field(default=None)


class OpenAIModelRun(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: Union[str, None] = Field(default=None)
    prompt_template: Union[str, None] = Field(default=None)
    transplant_organ: Union[str, None] = Field(default=None)
    diagnosis_description: str = Field(default=None)
    classification: Union[str, None] = Field(default=None)
    explanation: Union[str, None] = Field(default=None)
    probability_within_90_days: Union[str, None] = Field(default=None)
    openai_call_id: Union[str, None] = Field(default=None)
    created: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    system_fingerprint: Union[str, None] = Field(default=None)
    prompt_tokens: Union[str, None] = Field(default=None)
    completion_tokens: Union[str, None] = Field(default=None)
    total_tokens: Union[str, None] = Field(default=None)
