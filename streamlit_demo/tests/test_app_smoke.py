"""
Prueba de humo: la app sin errores y muestra de pestañas completas.

Utiliza streamlit.testing. Ejecutar desde streamlit_demo/:
    pytest tests/test_app_smoke.py -v
"""

import os
from streamlit.testing.v1 import AppTest

app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")

def _open_app():
    return AppTest.from_file(app_path, default_timeout = 120).run()

def test_app_ejecutada_sin_errores():
    at = _open_app()
    assert not at.exception, [e.value for e in at.exception]

def test_app_pestañas_completas():
    at = _open_app()
    assert len(at.tabs) == 3
