# Bitácora de Daily Scrums

Registra: Michelle. Cada integrante responde: ¿qué hice?, ¿qué haré?, ¿qué me bloquea?
Las sincronizaciones se hicieron por el grupo de WhatsApp del equipo y se registran solo los días en que
hubo sincronización. Los datos de avance (PR, merges y horas) se verifican en el historial de GitHub.

## Sprint 1 (10 – 14 oct)

### Daily – sáb 10 oct · inicio del Sprint 1 (medio: grupo de WhatsApp)

Reunión de arranque: se repartieron las tareas del Sprint 1 con la guía de trabajo del Corte 2
(pareja, piloto, copiloto y revisor de cada tarea).

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Revisé y aprobé el PR del Setup (#1) | Documentar la Tarea 1 · Data Ingestion Pipeline | Primera vez trabajando con ramas y Pull Requests desde Git Bash |
| Maria | — | Tarea 2 (reglas de validación de mora) | Ninguno |
| Michelle | Preparé la estructura del Corte 2 (tests, `docs/`, plantillas) y la guía de trabajo | Tarea 2 (tests y función de validación) y registro del Burndown | Ninguno |

### Daily – mar 13 oct · reorganización (medio: grupo de WhatsApp)

Desde el sábado solo se había fusionado la Tarea 1. Por los horarios de cada uno, el equipo decidió
repartir el trabajo por tareas completas para que nadie dependiera de otra persona en la misma tarea.

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Tarea 1 fusionada (PR #2) | Tareas 2 y 3 (validación de datos de mora y churn), con Maria de copiloto | Las Tareas 2 y 3 editan el mismo archivo (`validation.py`): deben hacerse en orden |
| Maria | — | Tareas 6 y 7 (dashboards) | Los dashboards se hacen después de los modelos |
| Michelle | Guía de trabajo y regla de revisión de PR | Tareas 4 y 5 (modelos), Velocity, Burndown y Retrospectivas | Ninguno |

### Daily – mié 14 oct · cierre del Sprint 1 (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Tarea 2 terminada y en PR (#3) | Tarea 3 (churn) | La Tarea 3 no podía empezar hasta que se revisara y fusionara el PR #3 (fusionado a las 11:59) |
| Maria | Copiloto en las Tareas 2 y 3 | Revisar los PR de las Tareas 4 y 5 | Ninguno |
| Michelle | Revisión y merge de los PR #3 y #4 | Cierre del Sprint 1 (PR #5) e inicio de las Tareas 4 y 5 | Ninguno |

## Sprint 2 (14 – 16 oct)

### Daily – jue 15 oct (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Copiloto en las Tareas 4 y 5; bitácora con las evidencias del Sprint 1 | Revisar el PR de la Tarea 6 | Ninguno |
| Maria | Revisión y merge de los PR #6 y #7 (Tareas 4 y 5) | Tarea 6 (dashboard de mora) | La Tarea 7 depende de que la Tarea 6 se revise y se fusione |
| Michelle | Tareas 4 y 5 terminadas en rama | Copiloto en las Tareas 6 y 7 | Las Tareas 4 y 5 esperaban revisión desde el miércoles |

### Daily – vie 16 oct · cierre del Sprint 2 (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Revisión y merge del PR #9 (Tarea 6) a las 05:36 y del PR #10 (Tarea 7) | Bitácora XP con las evidencias del Sprint 2 | Ninguno |
| Maria | Tarea 7 (dashboard de churn) | Cierre del Sprint 2 | La revisión del PR #9 llegó hasta el viernes en la mañana, por eso la Tarea 7 no se pudo cerrar el jueves. En el cierre, un commit se subió directo a `main` sin rama; los ajustes siguientes se hicieron en la rama `docs/ajustes-cierre-sprint2` (PR #12) |
| Michelle | Copiloto en las Tareas 6 y 7 | Revisión de los PR de cierre (#11 y #12) | Ninguno |
