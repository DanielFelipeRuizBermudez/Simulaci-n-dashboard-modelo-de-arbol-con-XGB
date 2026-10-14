# Sprints – Backlog, Velocity y Burndown

Escala de puntos: Fibonacci (1, 2, 3, 5, 8); deben coincidir con los de Trello.
Velocity = puntos de las historias que cumplen la Definition of Done.
Responsable de Velocity y Burndown: Michelle.
Gráficos: `python docs/scrum/burndown.py` (lee `docs/scrum/burndown.csv` y guarda los PNG en `docs/evidencias/`).

## Definition of Done

- [ ] Código en una rama `feature/...` trabajada en pareja (piloto/copiloto)
- [ ] Tests automatizados escritos y en verde (`pytest`)
- [ ] Pull Request revisado y aprobado por el integrante que no estuvo en la pareja
- [ ] Merge a `main` y tarjeta movida a *Done* en Trello

---

## Sprint 1 – Calidad de datos (plan: sáb 10 – dom 11 oct · real: sáb 10 – mié 14 oct)

**Objetivo del Sprint:** que ningún dato inválido llegue a los modelos de mora y churn. **Cumplido.**

| # | Historia | Rama | Pareja (piloto + copiloto) | Revisor PR | PR | Merge | Puntos | Estado |
|---|---|---|---|---|---|---|---|---|
| 0 | Setup Corte 2 (estructura, pytest, plantillas) | `chore/setup-corte2` | Michelle | Daniel | #1 | 10 oct 15:49 | – | Done |
| 1 | Data Ingestion Pipeline (ya cerrada, solo documentación) | `docs/sprint1-data-ingestion` | Daniel | Michelle | #2 | 10 oct 21:53 | – | Done |
| 2 | Data Transformation and Cleaning (Delinquency) | `feature/sprint1-delinquency-validation` | Daniel + Maria | Michelle | #3 | 14 oct 11:59 | 5 | Done |
| 3 | Data Transformation and Cleaning (Churn) | `feature/sprint1-churn-validation` | Daniel + Maria | Michelle | #4 | 14 oct 14:18 | 5 | Done |

- Puntos comprometidos: **10**
- Puntos completados: **10**
- Velocity real: **10 puntos (100 % de lo comprometido)**, en 5 días calendario en lugar de los 2 planeados.
- Resultado técnico: 32 tests automatizados en verde; `train_models.py` bloquea datos inválidos; refactor documentado en `docs/xp/refactor_01_validation.md`.

### Burndown (puntos restantes al final de cada día)

![Burndown Sprint 1](../evidencias/burndown_sprint1.png)

| Día | Fecha | Ideal | Real | Qué pasó |
|---|---|---|---|---|
| 0 | inicio | 10 | 10 | Setup fusionado (PR #1) y Tarea 1 documentada (PR #2) el sáb 10 |
| 1 | sáb 10 | 5 | 10 | Tarea 2 iniciada, sin cerrar |
| 2 | dom 11 | 0 | 10 | Sin merges (fin del plan) |
| 3 | lun 12 | 0 | 10 | Sin merges |
| 4 | mar 13 | 0 | 10 | Reorganización del equipo: cada pareja trabaja desde su PC en llamada |
| 5 | mié 14 | 0 | 0 | Tarea 2 (PR #3, 11:59) y Tarea 3 (PR #4, 14:18) fusionadas |

**Lectura:** la línea real se quedó plana 4 días y cayó de golpe el último. El equipo completó todo lo
comprometido (Velocity 100 %) pero con 3 días de retraso, porque el trabajo se concentró en una sola
sesión en lugar de repartirse en el Sprint. Ver Retrospectiva 1.

---

## Sprint 2 – Modelos y dashboards (mié 14 – jue 15 oct)

**Objetivo del Sprint:** que cada modelo tenga sus métricas guardadas y documentadas, y que cada
dashboard priorice clientes con reglas claras y probadas.

Regla de revisión: Cuando Daniel es piloto lo revisa Michelle, cuando Michelle es piloto  lo revisa Maria y cuando Maria es piloto lo revisa Daniel.

| # | Historia | Rama | Pareja (piloto + copiloto) | Revisor PR | Puntos | Estado |
|---|---|---|---|---|---|---|
| 4 | Predictive Model (Delinquency) | `feature/sprint2-delinquency-docs-validation` | Michelle + Daniel | Maria | 3 | |
| 5 | Predictive Model (Churn) | `feature/sprint2-churn-docs-validation` | Michelle + Daniel | Maria | 3 | |
| 6 | Delinquency Dashboard | `feature/sprint2-delinquency-dashboard` | Maria + Michelle | Daniel | 5 | |
| 7 | Churn Dashboard | `feature/sprint2-churn-dashboard` | Maria + Michelle | Daniel | 5 | |

- Puntos comprometidos: **16**
- Puntos completados: ___
- Velocity real: ___

Datos del Burndown: agregar las filas del Sprint 2 en `docs/scrum/burndown.csv` y correr el script.
