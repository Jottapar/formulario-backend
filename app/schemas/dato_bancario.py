from datetime import datetime
from sqlmodel import SQLModel

from app.schemas.banco import BancoRead
from app.schemas.tipo_cuenta_bancaria import TipoCuentaRead

class DatoBancarioCreate(SQLModel):
    num_cuenta: str
    banco_id: int
    tipo_cuenta_id: int


class DatoBancarioRead(SQLModel):
    id: int
    num_cuenta: str
    banco: BancoRead
    tipo_cuenta: TipoCuentaRead
    created_at: datetime 
    updated_at: datetime



