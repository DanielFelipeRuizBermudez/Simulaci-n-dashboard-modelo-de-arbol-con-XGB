# Bitácora técnica XP

Datos tomados del historial de Git/GitHub del repositorio.

Repositorio: https://github.com/DanielFelipeRuizBermudez/Simulaci-n-dashboard-modelo-de-arbol-con-XGB  
Pull Requests: https://github.com/DanielFelipeRuizBermudez/Simulaci-n-dashboard-modelo-de-arbol-con-XGB/pulls?q=is%3Apr

## 01 · Pair Programming

El autor del commit es el piloto y la línea `Co-authored-by:` es el copiloto. Las sesiones se hicieron
por llamada con pantalla compartida, cada pareja desde el PC del piloto. La evidencia de cada sesión es el commit con dos autores en GitHub
(`evidencias/t2_commit_coautor.png`, `evidencias/t3_commit_coautor.png`).

### Sprint 1

| Tarea | Subtarea | Fecha | Piloto (autor) | Copiloto (co-author) | Commit | Evidencia |
|---|---|---|---|---|---|---|
| 2 · Delinquency | Definir reglas de validación | 14 oct 11:07 | Daniel | Maria | `08f13a0` | `evidencias/t2_commit_coautor.png` |
| 2 · Delinquency | Quality checks (tests, rojo) | 14 oct 11:14 | Daniel | Maria | `09c6443` | `evidencias/t2_pytest_rojo.png` |
| 2 · Delinquency | Función de validación (R1–R6) | 14 oct 11:28 | Daniel | Maria | `dd6c79d` | |
| 2 · Delinquency | Transformaciones derivadas | 14 oct 11:31 | Daniel | Maria | `78339b8` | `evidencias/t2_pytest_verde.png` |
| 3 · Churn | Definir reglas de validación | 14 oct 12:17 | Daniel | Maria | `046a45b` | `evidencias/t3_commit_coautor.png` |
| 3 · Churn | Quality checks (tests, rojo) | 14 oct 12:21 | Daniel | Maria | `af01083` | `evidencias/t3_pytest_rojo.png` |
| 3 · Churn | Construir transformaciones | 14 oct 12:38 | Daniel | Maria | `f01f031` | |
| 3 · Churn | Bloquear datos inválidos en `train_models.py` | 14 oct 12:40 | Daniel | Maria | `e997a9b` | `evidencias/t3_pytest_verde.png` |
| 3 · Churn | Refactor XP 04 (esquema único) | 14 oct 12:46 | Daniel | Maria | `40d16ee` | `evidencias/t3_refactor_verde.png` |

Nota: el plan inicial alternaba piloto y copiloto por subtarea, sin embargo por tiempos nos vimos cortos y tuvimos que buscar una alternativa mas sencilla. En la práctica Daniel fue piloto de
todas las subtareas de las Tareas 2 y 3 y Maria copiloto.

### Sprint 2

| Tarea | Subtarea | Fecha | Piloto (autor) | Copiloto (co-author) | Commit | Evidencia |
|---|---|---|---|---|---|---|
| 4 · Model Delinquency | Tests del reporte (rojo) | | Michelle | Daniel | | |
| 4 · Model Delinquency | Reporte F2 en archivo | | Michelle | Daniel | | |
| 4 · Model Delinquency | Documentar resultados y limitaciones | | Michelle | Daniel | | |
| 5 · Model Churn | Tests del reporte (rojo) | | Michelle | Daniel | | |
| 5 · Model Churn | Reporte F1 en archivo | | Michelle | Daniel | | |
| 5 · Model Churn | Documentar resultados y limitaciones | | Michelle | Daniel | | |
| 6 · Delinquency Dashboard | Tests (rojo) | | Maria | | | |
| 6 · Delinquency Dashboard | Reglas 30/60 y versión del modelo | | Maria | | | |
| 6 · Delinquency Dashboard | Priorización en `app.py` | | Maria | | | |
| 7 · Churn Dashboard | Tests (rojo) | | Maria | | | |
| 7 · Churn Dashboard | Campos clave y alerta SHAP | | Maria | | | |
| 7 · Churn Dashboard | Priorización en `app.py` | | Maria | | | |

## 02 · Test-Driven Development

| Fecha | Rama | Archivo de tests | Antes (rojo) | Después (verde) | Evidencia |
|---|---|---|---|---|---|
| 14 oct | `feature/sprint1-delinquency-validation` | `tests/test_delinquency_validation.py` | Error: no existe `validation.py` (commit `09c6443`) | 15 passed (commit `78339b8`) | `t2_pytest_rojo.png`, `t2_pytest_verde.png`, `pytest_delinquency.txt` |
| 14 oct | `feature/sprint1-churn-validation` | `tests/test_churn_validation.py`, `tests/test_train_models_gate.py` | Error: faltan funciones de churn (commit `af01083`) | 32 passed (commit `40d16ee`) | `t3_pytest_rojo.png`, `t3_pytest_verde.png`, `pytest_churn.txt` |

El CI de GitHub Actions (`.github/workflows/tests.yml`) corre pytest en cada Pull Request. En cada PR el
check `tests` quedó en rojo con el commit de las pruebas y en verde al final:

| PR | CI en rojo | CI en verde |
|---|---|---|
| #3 · Delinquency | `evidencias/t2_CI_rojo.png` | `evidencias/t2_CI_verde.png` |
| #4 · Churn | `evidencias/t3_CI_rojo.png` | `evidencias/t3_CI_verde.png` |

## 03 · Integración continua y propiedad colectiva

| PR | Rama | Autores | Revisor | Revisión | Merge |
|---|---|---|---|---|---|
| #1 | `chore/setup-corte2` | Michelle | — | Sin revisión formal (configuración inicial) | 10 oct 15:49 |
| #2 | `docs/sprint1-data-ingestion` | Daniel | Michelle | Merge por Michelle | 10 oct 21:53 |
| #3 | `feature/sprint1-delinquency-validation` | Daniel, Maria | Michelle | Comentarios y aprobación registrados después del merge | 14 oct 11:59 |
| #4 | `feature/sprint1-churn-validation` | Daniel, Maria | Michelle | 3 comentarios de línea + Approve **antes** del merge | 14 oct 14:18 |

Seguimiento en Trello: `evidencias/trello_sprint1_en_progreso.png` (Tareas 2 y 3 en curso) y
`evidencias/trello_sprint1_done.jpg` (cierre del Sprint 1).

Evidencia: `evidencias/t2_PR_aprobado.jpeg`, `evidencias/t3_PR_revision.jpeg`, `evidencias/t3_PR_aprobado.png`.

## 04 · Simple Design y Refactorización

### Refactor 1: reglas de validación basadas en esquema único

Documentado en [`refactor_01_validation.md`](refactor_01_validation.md) (commit `40d16ee`).

- **Motivo:** `validate_delinquency_data` y `validate_churn_data` repetían la misma lógica.
- **Después:** una sola función `validate_data(df, schema)` y un esquema por modelo.
- **Verificación:** los 32 tests siguieron en verde sin modificar ninguno.
- **Evidencia:** `evidencias/t3_refactor_verde.png` (pytest) y `evidencias/t3_refactor_diff.png` (antes vs. después en GitHub).
