# Refactor 01 · Reglas de validación basadas en esquema

Práctica XP 04 · Simple Design & Refactoring
Tarea 3 · Sprint 1 · Rama `feature/sprint1-churn-validation`
Piloto: Daniel · Copiloto: Maria · Revisa: Michelle

## Motivo

Después de la Tarea 3, `validation.py` tenía dos funciones casi idénticas:
`validate_delinquency_data` y `validate_churn_data`. Las dos repetían los mismos
pasos (columnas faltantes, nulos, formato, rangos, duplicados y target binario)
y solo cambiaban las columnas y los rangos. Código duplicado significa:

- Un error corregido en una función hay que corregirlo también en la otra.
- Agregar un tercer modelo obligaría a copiar la función por tercera vez.

## Antes (commit de la subtarea "Construir transformaciones")

Dos funciones de unas 45 líneas cada una, con la misma lógica copiada:

```python
DELINQUENCY_RANGES = {...}
CHURN_RANGES = {...}

def validate_delinquency_data(df, require_target=True):
    errors = []
    required = [ID_COLUMN] + list(DELINQUENCY_RANGES)
    ...  # nulos, rangos, duplicados, target  (≈ 45 líneas)
    return errors

def validate_churn_data(df, require_target=True):
    errors = []
    required = [ID_COLUMN] + list(CHURN_RANGES)
    ...  # exactamente los mismos pasos       (≈ 45 líneas)
    return errors
```

## Después (commit `refactor:`)

Cada modelo declara su **esquema** y una sola función aplica las reglas:

```python
DELINQUENCY_SCHEMA = {"name": "mora",  "target": "defaulted_30_60_days", "ranges": {...}}
CHURN_SCHEMA       = {"name": "churn", "target": "churned_3_months",     "ranges": {...}}

def validate_data(df, schema, require_target=True):
    ...  # nulos, rangos, duplicados, target (una sola vez)

def validate_delinquency_data(df, require_target=True):
    return validate_data(df, DELINQUENCY_SCHEMA, require_target)

def validate_churn_data(df, require_target=True):
    return validate_data(df, CHURN_SCHEMA, require_target)
```

## Resultado

| Medida | Antes | Después |
|---|---|---|
| Líneas de `validation.py` | 183 | 154 |
| Copias de la lógica de validación | 2 | 1 |
| Pasos para agregar un modelo nuevo | Copiar ~45 líneas | Declarar un esquema |
| Funciones públicas que usan los tests y `train_models.py` | Sin cambios | Sin cambios |
| Tests | 32 en verde | 32 en verde (no se modificó ninguno) |

## Cómo se verificó que no se rompió nada

1. Antes del refactor: `pytest -v` → 32 passed.
2. Se reescribió `validation.py` sin tocar ningún test.
3. Después del refactor: `pytest -v` → 32 passed (evidencia en `docs/evidencias/pytest_churn.txt`).

Los tests actúan como red de seguridad: el comportamiento es el mismo y el código es más simple.
