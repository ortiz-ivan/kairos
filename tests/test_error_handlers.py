def test_404_error_page_contents(client):
    resp = client.get("/esta-ruta-no-existe-xyz")
    assert resp.status_code == 404
    data = resp.get_data(as_text=True)
    assert "Error 404" in data or "Página no encontrada" in data


# Nota: pruebas de 500 requieren una ruta que lance excepción; se puede añadir más adelante.
