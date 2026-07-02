class NotFoundError(Exception):
    """Se lanza cuando un recurso no existe en la DB"""
    pass

class ConflictError(Exception):
    """Se lanza cuando se viola una restriccion de unicidad"""
    pass

class BusinessError(Exception):
    """Se lanza pora errores de logica de negocio generales"""
    pass

