"""
Manejadores de errores centralizados para la aplicación Kairos.

Proporciona:
- Manejadores personalizados para 404, 500 y otros errores HTTP
- Logging automático de errores
- Respuestas amigables al usuario
"""

from flask import render_template

from utils.logging_config import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):
    """Registra los manejadores de errores en la aplicación Flask.

    Args:
        app: Instancia de Flask
    """

    @app.errorhandler(404)
    def handle_404(error):
        """Maneja errores 404 (No encontrado)."""
        logger.warning(f"404 - Página no encontrada: {error}")
        return (
            render_template(
                "error.html",
                error_code=404,
                error_title="Página no encontrada",
                error_message="La página que buscas no existe o ha sido eliminada.",
            ),
            404,
        )

    @app.errorhandler(403)
    def handle_403(error):
        """Maneja errores 403 (Acceso denegado)."""
        logger.warning(f"403 - Acceso denegado: {error}")
        return (
            render_template(
                "error.html",
                error_code=403,
                error_title="Acceso denegado",
                error_message="No tienes permisos para acceder a este recurso.",
            ),
            403,
        )

    @app.errorhandler(500)
    def handle_500(error):
        """Maneja errores 500 (Error interno del servidor)."""
        logger.error(f"500 - Error interno del servidor: {error}", exc_info=True)
        return (
            render_template(
                "error.html",
                error_code=500,
                error_title="Error interno del servidor",
                error_message="Algo salió mal. El equipo técnico ha sido notificado.",
            ),
            500,
        )

    @app.errorhandler(400)
    def handle_400(error):
        """Maneja errores 400 (Solicitud malformada)."""
        logger.warning(f"400 - Solicitud malformada: {error}")
        return (
            render_template(
                "error.html",
                error_code=400,
                error_title="Solicitud inválida",
                error_message="La solicitud que enviaste no es válida. Verifica los datos e intenta de nuevo.",
            ),
            400,
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Maneja excepciones genéricas no capturadas."""
        logger.error(
            f"Excepción no manejada: {type(error).__name__}: {error}", exc_info=True
        )

        # En desarrollo, retornar el error completo; en producción, mensaje genérico
        import os

        is_production = (
            os.environ.get("FLASK_ENV") == "production"
            or os.environ.get("PRODUCTION") == "1"
        )

        if is_production:
            return (
                render_template(
                    "error.html",
                    error_code=500,
                    error_title="Error inesperado",
                    error_message="Ocurrió un error inesperado. Por favor, intenta más tarde.",
                ),
                500,
            )
        else:
            # En desarrollo, mostrar el error completo
            return (
                render_template(
                    "error.html",
                    error_code=500,
                    error_title="Error inesperado (Desarrollo)",
                    error_message=f"{type(error).__name__}: {str(error)}",
                ),
                500,
            )
