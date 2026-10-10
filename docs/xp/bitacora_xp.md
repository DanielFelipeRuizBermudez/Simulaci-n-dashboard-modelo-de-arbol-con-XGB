# Bitácora técnica XP

## 01 · Pair Programming

Una fila por subtarea de Trello. El autor del commit es el piloto y la línea `Co-authored-by:` es el copiloto.

### Sprint 1

| Tarea | Subtarea | Fecha | Piloto | Copiloto | Commit | Evidencia |
|---|---|---|---|---|---|---|
| 2 · Delinquency | Definir reglas de validación | | Maria | Michelle | | `evidencias/pairing_t2.jpg` |
| 2 · Delinquency | Quality checks (tests) | | Michelle | Maria | | |
| 2 · Delinquency | Función de validación | | Michelle | Maria | | |
| 2 · Delinquency | Transformaciones derivadas | | Maria | Michelle | | |
| 3 · Churn | Definir reglas de validación | | Daniel | Maria | | `evidencias/pairing_t3.jpg` |
| 3 · Churn | Quality checks (tests) | | Daniel | Maria | | |
| 3 · Churn | Transformaciones (uso de producto, quejas) | | Maria | Daniel | | |
| 3 · Churn | Bloquear datos inválidos en `train_models.py` | | Maria | Daniel | | |

### Sprint 2

| Tarea | Subtarea | Fecha | Piloto | Copiloto | Commit | Evidencia |
|---|---|---|---|---|---|---|
| 4 · Model Delinquency | Validar con datos históricos (reporte F2) | | Daniel | Maria | | |
| 4 · Model Delinquency | Documentar resultados y limitaciones | | Maria | Daniel | | |
| 5 · Model Churn | Evaluar F1 en validación (reporte) | | Maria | Michelle | | |
| 5 · Model Churn | Documentar resultados y limitaciones | | Michelle | Maria | | |
| 6 · Delinquency Dashboard | Reglas de alerta 30/60 | | Michelle | Daniel | | |
| 6 · Delinquency Dashboard | Fórmula de priorización | | Daniel | Michelle | | |
| 6 · Delinquency Dashboard | Versión de datos/modelo | | Michelle | Daniel | | |
| 6 · Delinquency Dashboard | Test de conexión | | Daniel | Michelle | | |
| 7 · Churn Dashboard | Indicadores y campos clave | | Daniel | Maria | | |
| 7 · Churn Dashboard | Fórmula de priorización | | Maria | Daniel | | |
| 7 · Churn Dashboard | Alerta por variable SHAP | | Daniel | Maria | | |
| 7 · Churn Dashboard | Test de conexión | | Maria | Daniel | | |

## 02 · Test-Driven Development

| Fecha | Rama | Archivo de tests | Antes (rojo) | Después (verde) | Evidencia |
|---|---|---|---|---|---|
| | `feature/sprint1-delinquency-validation` | `tests/test_delinquency_validation.py` | | | `evidencias/pytest_delinquency.txt` |
| | `feature/sprint1-churn-validation` | `tests/test_churn_validation.py` | | | |

## 03 · Integración continua y propiedad colectiva

| PR | Rama | Autores | Revisor | Comentarios de revisión | Fecha de merge |
|---|---|---|---|---|---|
| #1 | `chore/setup-corte2` | | | | |
| #2 | `docs/sprint1-data-ingestion` | Daniel | Michelle | | |
| #3 | `feature/sprint1-delinquency-validation` | Maria, Michelle | Daniel | | |
| #4 | `feature/sprint1-churn-validation` | Daniel, Maria | Michelle | | |

## 04 · Simple Design y Refactorización

### Refactor 1: ___

- **Motivo:**
- **Antes:** (fragmento de código o enlace al commit)
- **Después:** (fragmento de código o enlace al commit)
- **Cómo se verificó que no se rompió nada:** los tests siguen en verde (`pytest -v`).
