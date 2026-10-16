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
| 4 · Model Delinquency | Tests de validación del modelo (rojo) | 14 oct 16:21 | Michelle | Daniel | `5bb2bc2` | `evidencias/t4_pytest_rojo.png` |
| 4 · Model Delinquency | `evaluate_models.py` y reporte F2 | 14 oct 16:29 | Michelle | Daniel | `535d98f` | `evidencias/t4_pytest_verde.png` |
| 4 · Model Delinquency | Documentar resultados, SHAP y limitaciones | 14 oct 16:30 | Michelle | Daniel | `448233f` | `streamlit_demo/docs/model_delinquency.md` |
| 5 · Model Churn | Tests de evaluación F1 (rojo) | 14 oct 16:57 | Michelle | Daniel | `19d771e` | `evidencias/t5_pytest_rojo.png` |
| 5 · Model Churn | Reporte F1 y matriz de confusión | 14 oct 17:00 | Michelle | Daniel | `c87c13e` | `evidencias/t5_pytest_verde.png` |
| 5 · Model Churn | Documentar resultados, SHAP y limitaciones | 14 oct 17:01 | Michelle | Daniel | `f23c89f` | `streamlit_demo/docs/model_churn.md` |
| 6 · Delinquency Dashboard | Tests de conexión, alertas 30/60 y prioridad (rojo) | 15 oct 21:59 | Maria | Michelle | `89ac833` | `evidencias/t6_pytest_rojo.png` |
| 6 · Delinquency Dashboard | Reglas de alerta 30/60 y versión del modelo | 15 oct 22:10 | Maria | Michelle | `ffde42c` | `evidencias/t6_pytest_verde.png` |
| 6 · Delinquency Dashboard | Alerta, `priority_score` y versión en `app.py` | 15 oct 22:26 | Maria | Michelle | `a440101` | `evidencias/t6_dashboard.png` |
| 7 · Churn Dashboard | Tests de conexión y alerta SHAP (rojo) | 16 oct 10:28 | Maria | Michelle | `85960c9` | `evidencias/t7_pytest_rojo.png` |
| 7 · Churn Dashboard | Campos clave y variable SHAP que dispara la alerta | 16 oct 10:34 | Maria | Michelle | `33d2647` | |
| 7 · Churn Dashboard | `priority_score` y alerta SHAP en `app.py` | 16 oct 10:48 | Maria | Michelle | `5d0ccf4` | `evidencias/t7_dashboard.png` |

En el Sprint 2 cada pareja trabajó desde el PC del piloto: Michelle con Daniel en los modelos y Maria
con Michelle en los dashboards. Todos los commits registran al copiloto con `Co-authored-by:`.

## 02 · Test-Driven Development

| Fecha | Rama | Archivo de tests | Antes (rojo) | Después (verde) | Evidencia |
|---|---|---|---|---|---|
| 14 oct | `feature/sprint1-delinquency-validation` | `tests/test_delinquency_validation.py` | Error: no existe `validation.py` (commit `09c6443`) | 15 passed (commit `78339b8`) | `t2_pytest_rojo.png`, `t2_pytest_verde.png`, `pytest_delinquency.txt` |
| 14 oct | `feature/sprint1-churn-validation` | `tests/test_churn_validation.py`, `tests/test_train_models_gate.py` | Error: faltan funciones de churn (commit `af01083`) | 32 passed (commit `40d16ee`) | `t3_pytest_rojo.png`, `t3_pytest_verde.png`, `pytest_churn.txt` |
| 14 oct | `feature/sprint2-delinquency-docs-validation` | `tests/test_model_delinquency.py` | Error: no existe `evaluate_models.py` (commit `5bb2bc2`) | 40 passed (commit `535d98f`) | `t4_pytest_rojo.png`, `t4_pytest_verde.png` |
| 14 oct | `feature/sprint2-churn-docs-validation` | `tests/test_model_churn.py` | Falla: no existe el reporte de churn (commit `19d771e`) | 46 passed (commit `c87c13e`) | `t5_pytest_rojo.png`, `t5_pytest_verde.png` |
| 15 oct | `feature/sprint2-delinquency-dashboard` | `tests/test_delinquency_dashboard.py` | Error: no existe `dashboard_logic.py` (commit `89ac833`) | 52 (commit `a440101`) | `t6_pytest_rojo.png`, `t6_pytest_verde.png` |
| 16 oct | `feature/sprint2-churn-dashboard` | `tests/test_churn_dashboard.py` | Error: faltan las funciones de churn del dashboard (commit `85960c9`) | 57 passed, suite completa (commit `5d0ccf4`) | `t7_pytest_rojo.png`, `t7_pytest_verde.png` |

Al cierre del Sprint 2 el proyecto tiene 57 tests automatizados en verde.

El CI de GitHub Actions (`.github/workflows/tests.yml`) corre pytest en cada Pull Request. En cada PR el
check `tests` quedó en rojo con el commit de las pruebas y en verde al final:

| PR | CI en rojo | CI en verde |
|---|---|---|
| #3 · Delinquency | `evidencias/t2_CI_rojo.png` | `evidencias/t2_CI_verde.png` |
| #4 · Churn | `evidencias/t3_CI_rojo.png` | `evidencias/t3_CI_verde.png` |

En el Sprint 2 el check `tests` quedó en verde antes del merge en los PR #6, #7, #9 y #10 (pestaña
*Checks* de cada PR).

## 03 · Integración continua y propiedad colectiva

| PR | Rama | Autores | Revisor | Revisión | Merge |
|---|---|---|---|---|---|
| #1 | `chore/setup-corte2` | Michelle | — | Sin revisión formal (configuración inicial) | 10 oct 15:49 |
| #2 | `docs/sprint1-data-ingestion` | Daniel | Michelle | Merge por Michelle | 10 oct 21:53 |
| #3 | `feature/sprint1-delinquency-validation` | Daniel, Maria | Michelle | Comentarios y aprobación registrados después del merge | 14 oct 11:59 |
| #4 | `feature/sprint1-churn-validation` | Daniel, Maria | Michelle | 3 comentarios de línea + Approve **antes** del merge | 14 oct 14:18 |
| #5 | `docs/cierre-sprint1` | Michelle | Maria | Merge por Maria | 14 oct 15:54 |
| #6 | `feature/sprint2-delinquency-docs-validation` | Michelle, Daniel | Maria | 3 comentarios de línea + Approve antes del merge | 15 oct 21:10 |
| #7 | `feature/sprint2-churn-docs-validation` | Michelle, Daniel | Maria | 2 comentarios de línea + Approve antes del merge | 15 oct 21:18 |
| #8 | `docs/evidencias-sprint1` | Daniel | Maria | Merge por Maria | 16 oct 11:13 |
| #9 | `feature/sprint2-delinquency-dashboard` | Maria, Michelle | Daniel | 2 comentarios de línea + Approve antes del merge | 16 oct 05:36 |
| #10 | `feature/sprint2-churn-dashboard` | Maria, Michelle | Daniel | Comentarios de línea + Approve antes del merge | 16 oct 11:09 |

Seguimiento en Trello: `evidencias/trello_sprint1_en_progreso.png` (Tareas 2 y 3 en curso) y
`evidencias/trello_sprint1_done.jpg` (cierre del Sprint 1); `evidencias/t4_done.png`, `evidencias/t5_done.png` y
`evidencias/modelo_delinquiency_done.png` (avance del Sprint 2).

Evidencia: `evidencias/t2_PR_aprobado.jpeg`, `evidencias/t3_PR_revision.jpeg`, `evidencias/t3_PR_aprobado.png`,
`evidencias/t4_PR_revision.png`, `evidencias/t5_PR_revision.png`, `evidencias/t6_PR_aprobado.png`, `evidencias/t7_PR_aprobado.png`.

## 04 · Simple Design y Refactorización

### Refactor 1: reglas de validación basadas en esquema único

Documentado en [`refactor_01_validation.md`](refactor_01_validation.md) (commit `40d16ee`).

- **Motivo:** `validate_delinquency_data` y `validate_churn_data` repetían la misma lógica.
- **Después:** una sola función `validate_data(df, schema)` y un esquema por modelo.
- **Verificación:** los 32 tests siguieron en verde sin modificar ninguno.
- **Evidencia:** `evidencias/t3_refactor_verde.png` (pytest) y `evidencias/t3_refactor_diff.png` (antes vs. después en GitHub).
