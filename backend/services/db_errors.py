from sqlalchemy.exc import SQLAlchemyError  # pyrefly: ignore [missing-import]


def db_error_detail(error: SQLAlchemyError, fallback: str) -> str:
    """Devuelve el mensaje especifico de PostgreSQL cuando esta disponible."""
    original = getattr(error, "orig", None)
    diagnostic = getattr(original, "diag", None)
    message = getattr(diagnostic, "message_primary", None)

    if not message and original is not None:
        message = str(original).splitlines()[0]

    return message.strip() if message else fallback