# Sprints – Backlog, Velocity y Burndown

Escala de puntos: Fibonacci (1, 2, 3, 5, 8); deben coincidir con los de Trello.
Velocity = puntos de las historias que cumplen la Definition of Done.
Responsable de Velocity y Burndown: Michelle.

## Definition of Done

- [ ] Código en una rama `feature/...` trabajada en pareja (piloto/copiloto alternando por subtarea)
- [ ] Tests automatizados escritos y en verde (`pytest`)
- [ ] Pull Request revisado y aprobado por el integrante que no estuvo en la pareja
- [ ] Merge a `main` y tarjeta movida a *Done* en Trello

---

## Sprint 1 – Calidad de datos (sáb 10 – dom 11 oct)

**Objetivo del Sprint:** que ningún dato inválido llegue a los modelos de mora y churn.

| # | Historia | Rama | Pareja | Revisor PR | Puntos | Estado |
|---|---|---|---|---|---|---|
| 1 | Data Ingestion Pipeline (ya cerrada) | `docs/sprint1-data-ingestion` | Daniel | Michelle | – | |
| 2 | Data Transformation and Cleaning (Delinquency) | `feature/sprint1-delinquency-validation` | Maria + Michelle | Daniel | 5 | |
| 3 | Data Transformation and Cleaning (Churn) | `feature/sprint1-churn-validation` | Daniel + Maria | Michelle | 5 | |

- Puntos comprometidos: **10**
- Puntos completados: ___
- Velocity real: ___ (___ % de lo comprometido)

### Datos del Burndown (puntos restantes al final de cada día)

| Día | Fecha | Ideal | Real |
|---|---|---|---|
| 0 | inicio | 10 | 10 |
| 1 | sáb 10 | 5 | |
| 2 | dom 11 | 0 | |

---

## Sprint 2 – Modelos y dashboards (lun 12 – mar 13 oct)

**Objetivo del Sprint:** ___

| # | Historia | Rama | Pareja | Revisor PR | Puntos | Estado |
|---|---|---|---|---|---|---|
| 4 | Predictive Model (Delinquency) | `feature/sprint2-delinquency-docs-validation` | Daniel + Maria | Michelle | 3 | |
| 5 | Predictive Model (Churn) | `feature/sprint2-churn-docs-validation` | Maria + Michelle | Daniel | 3 | |
| 6 | Delinquency Dashboard | `feature/sprint2-delinquency-dashboard` | Michelle + Daniel | Maria | 5 | |
| 7 | Churn Dashboard | `feature/sprint2-churn-dashboard` | Daniel + Maria | Michelle | 5 | |

- Puntos comprometidos: **16**
- Puntos completados: ___
- Velocity real: ___

| Día | Fecha | Ideal | Real |
|---|---|---|---|
| 0 | inicio | 16 | 16 |
| 1 | lun 12 | 8 | |
| 2 | mar 13 | 0 | |
