"""Excepciones personalizadas para el proyecto"""

class APIConnectionError(Exception):
    """Error al conectar con la API externa"""
    pass

class APIResponseError(Exception):
    """Error en la respuesta de la API"""
    pass

class DataValidationError(Exception):
    """Error en la validación de datos"""
    pass

class FileProcessingError(Exception):
    """Error al procesar archivos"""
    pass

class ConfigurationError(Exception):
    """Error en la configuración del sistema"""
    pass
