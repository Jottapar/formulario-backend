
class NotFoundError(Exception):
    def __init__(self, entity: str, id: int | None = None):
        self.id = id
        self.entity = entity
        message = f'{entity} con id {id} no encontrado' if id is not None else f'{entity} no encontrado'
        super().__init__(message)

class AlreadyExistsError(Exception):
    def __init__(self,entity: str, field: str, value: str):
        self.entity = entity
        self.field = field
        self.value = value
        message = f'{entity} con {field}={value} ya existe'
        super().__init__(message)

class BussinesError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)