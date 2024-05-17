from sqlmodel import create_engine, Session

DB_URL = "sqlite:///db.sqlite"
engine = create_engine(DB_URL, echo=True)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
