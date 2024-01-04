from app import SessionLocal


def get_session() -> SessionLocal:
    """取得資料庫 Session

    Returns:
        SessionLocal: SessionLocal

    Yields:
        Iterator[SessionLocal]: Session
    """

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
