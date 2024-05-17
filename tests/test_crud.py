from sqlmodel import SQLModel, create_engine, select, Session, StaticPool
from webapp.main import app
from webapp import db, models, crud
import pytest

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL, 
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
    )

@pytest.fixture
def startup():
    SQLModel.metadata.create_all(bind=test_engine)
    yield 1
    SQLModel.metadata.drop_all(bind=test_engine)

# def teardown():
#     SQLModel.metadata.drop_all(bind=test_engine)

def override_get_session():
    test_session = Session(test_engine)
    try:
        yield test_session
    finally:
        test_session.close()

app.dependency_overrides[db.get_session] = override_get_session


def test_db_write_create_user(startup):
    test_session = next(override_get_session())
    test_user_create = models.UserInDB(
        email='testuser@test.com', 
        hashed_password='this is a mock hash'
        )
    test_user_in_db = crud.db_write_create_user(
        session=test_session, 
        db_user=test_user_create
        )
    assert test_user_in_db.id == 1
    assert test_user_in_db.email == 'testuser@test.com'
    assert test_user_in_db.hashed_password == 'this is a mock hash'


def test_db_read_user_by_email(startup):
    test_session = next(override_get_session())
    test_user_create = models.UserInDB(
        email='testuser@test.com', 
        hashed_password='this is a mock hash'
        )
    test_user_in_db = crud.db_write_create_user(
        session=test_session, 
        db_user=test_user_create
        )
    test_user_to_search = models.UserBasic(email=test_user_create.email)
    test_user_in_db = crud.db_read_user_by_email(
        session=test_session, 
        user_basic=test_user_to_search
        )
    assert test_user_in_db.id == 1
    assert test_user_in_db.email == 'testuser@test.com'
    assert test_user_in_db.hashed_password == 'this is a mock hash'
