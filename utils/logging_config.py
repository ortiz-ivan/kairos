"""
Configuración centralizada de logging para la aplicación Kairos.

Proporciona:
- Logging a archivo con rotación
- Logging a consola
- Diferentes niveles según el ambiente
- Formato estructurado de logs
"""

import logging
import logging.handlers
import os


def setup_logging(app):
    """Configura el logging centralizado para la aplicación.

    Args:
        app: Instancia de Flask
    """

    # Crear directorio de logs si no existe
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Determinar nivel de logging según el ambiente
    is_production = (
        os.environ.get("FLASK_ENV") == "production"
        or os.environ.get("PRODUCTION") == "1"
    )
    log_level = logging.INFO if is_production else logging.DEBUG

    # Formato de logs
    log_format = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Logger raíz de la aplicación
    logger = logging.getLogger("kairos")
    logger.setLevel(log_level)

    # Handler para archivo con rotación (máx 5 archivos de 10MB cada uno)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir, "kairos.log"),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Handler para errores críticos en archivo separado
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir, "kairos_errors.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    logger.addHandler(error_handler)

    # Handler para consola (solo en desarrollo)
    if not is_production:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

    # Reducir verbosidad de librerías externas
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    return logger


def get_logger(name):
    """Obtiene un logger con el nombre especificado.

    Args:
        name: Nombre del logger (típicamente __name__)

    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(f"kairos.{name}")
