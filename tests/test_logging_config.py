import logging
import os
import sys

from flask import Flask

sys.path.insert(0, os.getcwd())

from utils.logging_config import get_logger, setup_logging  # noqa: E402


def test_setup_logging_creates_files(tmp_path, monkeypatch):
    # Ejecutar setup_logging usando la app de Flask
    app = Flask(__name__)
    # Forzar cwd al proyecto (ya lo es en entorno de test)
    logger = setup_logging(app)
    assert logger is not None

    logs_dir = os.path.join(os.getcwd(), "logs")
    assert os.path.isdir(logs_dir)
    assert os.path.exists(os.path.join(logs_dir, "kairos.log"))
    assert os.path.exists(os.path.join(logs_dir, "kairos_errors.log"))


def test_get_logger_namespace():
    logger = get_logger("tests")
    assert isinstance(logger, logging.Logger)
    assert logger.name.startswith("kairos.")
