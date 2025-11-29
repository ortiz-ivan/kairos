#!/usr/bin/env python
"""
Script de utilidad para tareas de desarrollo comunes.

Uso:
    python dev.py test          # Ejecutar tests
    python dev.py test -v       # Verbose
    python dev.py test --cov    # Con cobertura
    python dev.py lint          # Ejecutar pre-commit
    python dev.py lint --fix    # Ejecutar pre-commit (auto-fix)
    python dev.py format        # Formatear con Black
    python dev.py format --check # Verificar formato sin cambios
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def run_command(cmd, *args):
    """Ejecuta un comando y muestra su output."""
    full_cmd = [cmd] + list(args)
    print(f"▶ {' '.join(full_cmd)}")
    result = subprocess.run(full_cmd, cwd=PROJECT_ROOT)
    return result.returncode


def test(*args):
    """Ejecutar pytest."""
    cmd = ["pytest"]
    if "--cov" in args:
        cmd.extend(["--cov=.", "--cov-report=term-missing"])
        args = [a for a in args if a != "--cov"]
    cmd.extend(args)
    return run_command(*cmd)


def lint(*args):
    """Ejecutar pre-commit."""
    if "--fix" in args or not args:
        cmd = ["pre-commit", "run", "--all-files"]
    else:
        cmd = ["pre-commit", "run", "--all-files"]
    return run_command(*cmd)


def format_code(*args):
    """Formatear código con Black."""
    cmd = ["black", "."]
    if "--check" in args:
        cmd.append("--check")
    return run_command(*cmd)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else ()

    if command == "test":
        sys.exit(test(*args))
    elif command == "lint":
        sys.exit(lint(*args))
    elif command == "format":
        sys.exit(format_code(*args))
    else:
        print(f"❌ Comando desconocido: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
