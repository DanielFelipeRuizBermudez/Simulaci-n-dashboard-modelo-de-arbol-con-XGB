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

## Sprint 3 (11 – 15 nov)

### Sprint Planning – lun 9 nov (medio: reunión por Teams)

Se revisó la ruta de trabajo de la entrega final y se repartieron las historias del Sprint 3 con pareja,
revisor y fecha límite: Sol call queue (Michelle + Daniel, revisa Maria, jue 12), End to end validation
(Maria + Michelle, revisa Daniel, vie 13), Post deployment monitoring (Daniel + Maria, revisa Michelle, sáb 14)
y Release v1.0 (Michelle + Daniel, revisa Maria, dom 15). Las tarjetas se ajustaron en Trello el mar 10 y
pasaron a *To do* el mié 11 (ver `docs/evidencias/trello_sprint3_planning.png`).

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | — | Copiloto de Sol call queue; revisar End to end validation; Post deployment monitoring | Ninguno |
| Maria | — | Revisar Sol call queue; End to end validation | Ninguno |
| Michelle | — | Sol call queue; Burndown y dailies del Sprint 3 | Ninguno |

### Daily – mierc nov · inicio del Sprint 3 (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Copiloto de Sol call queue con Michelle | Revisar End to end validation; Post deployment monitoring (fecha límite sáb 14) | Ninguno |
| Maria | — | Revisar Sol call queue (PR #15); End to end validation (fecha límite vie 13) | Ninguno |
| Michelle | Sol call queue con Daniel: pruebas en rojo (15:09), código en verde (15:23) y PR #15 abierto para Maria | Merge de Sol call queue cuando pase el CI; copiloto de Maria en End to end validation | Incidente de GitHub Actions desde las 15:48: el CI del PR #15 no arrancó. Mitigación: pruebas locales en verde y revisión del código mientras tanto. La app no abría con Streamlit 1.38 (`st.segmented_control`); se subió el mínimo a 1.40 |

### Daily – jue 12 nov (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Copiloto de Sol call queue (fusionada) | Revisar End to end validation | Ninguno |
| Maria | Revisión, aprobación y merge del PR #15 (Sol call queue) a las 15:57, el día de su fecha límite | End to end validation con Michelle | Ninguno |
| Michelle | Sol call queue fusionada | Copiloto de Maria en End to end validation | Ninguno |

> vie 13 nov: no hubo daily. End to end validation no avanzó ese día (ver Retrospectiva 3).

### Daily – sáb 14 nov (medio: grupo de WhatsApp)

Desde el jueves solo se había fusionado Sol call queue: End to end validation no avanzó el viernes, por lo que
se terminó el sábado y Post deployment monitoring se hizo esa misma noche.

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Revisión, aprobación y merge del PR #17 (End to end validation) a las 23:11. Post deployment monitoring con Maria: pruebas en rojo (23:38), código en verde con 93 pruebas (23:45), PR #18 abierto para Michelle (23:47) y evidencias (23:54) | Mover Post deployment monitoring a *Done* cuando se fusione; copiloto de Michelle en Release v1.0 | Post deployment monitoring dependía del merge de End to end validation; se entregó el día de su fecha límite pero a última hora y la revisión quedó para el domingo |
| Maria | End to end validation con Michelle: prueba de punta a punta (22:43), pruebas en el CI en cada PR (22:44), evidencias (22:57) y PR #17 abierto para Daniel. Copiloto de Daniel en Post deployment monitoring | Revisar Release v1.0 | End to end validation se entregó un día después de su fecha límite |
| Michelle | Copiloto de Maria en End to end validation | Revisar el PR #18 (Post deployment monitoring) | Ninguno |

### Daily – dom 15 nov · cierre del Sprint 3 (medio: grupo de WhatsApp)

| Integrante | ¿Qué hice? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Daniel | Post deployment monitoring en *Done*. Aportes a la Retrospectiva 3: avisar cuando una tarea no va a cumplir su fecha, no subir PR a última hora y mantener la revisión en menos de 24 h | Copiloto de Michelle en Release v1.0 (README y CHANGELOG) | Ninguno |
| Maria | Aportes a la Retrospectiva 3: arrancar cada tarea un día antes de su fecha límite, no encadenar tareas sin margen y mantener separadas en el CI las pruebas unitarias y las de punta a punta | Revisar el PR de Release v1.0 | Ninguno |
| Michelle | Revisión, aprobación y merge del PR #18 (Post deployment monitoring) a las 14:00. Release v1.0 con Daniel: README, CHANGELOG, Sprint Review y Retrospectiva 3. Aportes a la Retrospectiva 3: reportar la daily antes de las 9 p. m. del mismo día, no dejar dailies y Burndown para el final, mantener TDD y la aprobación antes del merge | Etiqueta `v1.0` cuando se fusione el PR #16 | Release v1.0 se completó el domingo en la noche; el merge del PR #16 depende de la revisión de Maria |