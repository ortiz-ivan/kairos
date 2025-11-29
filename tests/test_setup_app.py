import os


def test_create_app_and_404(client):
    # Petición a ruta inexistente debe devolver 404 y usar la plantilla de error
    resp = client.get("/ruta-que-no-existe-para-test")
    assert resp.status_code == 404
    data = resp.get_data(as_text=True)
    # La plantilla muestra "Error 404" en el título/card
    assert "Error 404" in data or "Página no encontrada" in data


def test_logs_directory_exists():
    # El setup de logging crea logs/ y kairos.log
    assert os.path.isdir(os.path.join(os.getcwd(), "logs"))
    assert os.path.exists(os.path.join(os.getcwd(), "logs", "kairos.log"))
