from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings
import app.models
 

# 1. El ENGINE: la fábrica de conexiones. Se crea UNA sola vez.
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # imprime el SQL que ejecuta (útil para aprender)
)


# 2. Crea las tablas a partir de los models. Se llama al arrancar la app.
def init_db() -> None:
    SQLModel.metadata.create_all(engine)


# 3. La DEPENDENCY: presta una session por petición y la cierra sola.
def get_session():
    with Session(engine) as session:
        yield session