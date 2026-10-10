# Pruebas automatizadas (TDD)

Las pruebas se ejecutan desde la carpeta `streamlit_demo/`:

```bash
pytest -v
```

Convención: un archivo `test_<modulo>.py` por módulo. Primero se escribe y
se sube el test (rojo) y después la implementación que lo hace pasar (verde).
