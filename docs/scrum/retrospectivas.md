# Retrospectivas (Start / Stop / Continue)

Duración: 10–15 minutos al cierre de cada Sprint. Participan: todos. Se documenta aquí.

## Retrospectiva Sprint 1 – mié 14 oct, 15:12 pm


| Start (empezar a hacer) | Stop (dejar de hacer) | Continue (seguir haciendo) |
|---|---|---|
| Hacer un merge al día como mínimo, para que el Burndown baje de forma gradual | Hacer merge antes de que el revisor comente y apruebe (pasó en el PR #3) | Escribir los tests antes que el código (rojo → verde) |
| Hacer y registrar la Daily cada día de Sprint | Dejar todo el trabajo para el último día del Sprint | Un commit por subtarea, con `Co-authored-by:` |
| Tomar la captura del pairing al inicio de cada sesión | Planear Sprints de 2 días sin margen para imprevistos | Revisar con comentarios en líneas concretas (como en el PR #4) |
| Alternar piloto y copiloto dentro de cada tarea | | Trabajar por llamada con pantalla compartida desde el PC de cada uno |

**Acciones de mejora para el Sprint 2:**

1. El revisor siempre comenta y aprueba **antes** de hacer el merge (regla aplicada desde el PR #4).
2. Michelle registra los puntos restantes cada noche en `docs/scrum/burndown.csv`.
3. Las Tareas 4 y 6 empiezan en paralelo (no dependen entre sí) para repartir el trabajo en los días del Sprint.

## Retrospectiva Sprint 2 – vie 16 oct

| Start (empezar a hacer) | Stop (dejar de hacer) | Continue (seguir haciendo) |
|---|---|---|
| Repartir los merges en los días del Sprint para que el Burndown baje de forma gradual | No realizar tareas 6 y 7 con antigüedad | Escribir los tests antes que el código: el test de mora detectó que faltaban los umbrales en `dashboard_logic.py` |
| Acordar un plazo para revisar los PR y avisar cuando se abre uno, sobre todo si otra tarea depende de él | Dejar PR sin revisar para día siguiente: el PR #9 (Tarea 6) se fusionó el viernes 16 y la Tarea 7 no pudo cerrarse el jueves 15 | Un commit por subtarea, con `Co-authored-by:` |
| Revisar `git status` desde la raíz del repo antes de cada commit, para no dejar evidencias sin subir | Editar archivos que vienen listos sin volver a correr `pytest` | Revisar con comentarios en líneas concretas y aprobar antes del merge |
| Empezar primero las tareas de las que dependen otras | Planear Sprints de 2 días sin margen para las dependencias | Trabajar por llamada con pantalla compartida para mantener pair programming|

**Lecciones aprendidas y plan de mejora:**

1. Las tareas que dependen de otras se empiezan el primer día del Sprint, y el PR del que depende otra tarea se revisa de inmediato: la Tarea 7 quedó sin cerrar el jue 15 porque el PR #9 de la Tarea 6 se fusionó hasta el vie 16.
2. Los tests detectan errores de copia o edición: correr `pytest` después de cada cambio, incluso si solo se tocaron comentarios.
3. El modelo de mora marca al 85 % de los clientes y el F1 del churn es 0,296: revisar el umbral con el equipo de cobranza antes de llevar los modelos a producción.
4. Subir las evidencias (capturas, pairing, Trello) junto con el commit de cada tarea.
5. Registrar el Burndown cada noche (acción pendiente desde la Retrospectiva 1).

## Retrospectiva Sprint 3 – dom 15 nov


**Datos del Sprint:** 16 de 16 puntos (Velocity 100 %). P1 a tiempo; P2 y P3 un día después de su fecha
límite. 93 pruebas automatizadas. Impedimentos: incidente de GitHub Actions el mié 11 (el CI del PR #15 no
arrancó), la app no abría con Streamlit 1.38 y el Sprint arrancó un día tarde.

| Start (empezar a hacer) | Stop (dejar de hacer) | Continue (seguir haciendo) |
|---|---|---|
| Avisar en el grupo apenas una tarea no va a cumplir su fecha: la P2 llegó un día tarde y se supo hasta la noche del sábado | Subir los PR a última hora de la noche: el #17 (P2) se abrió cerca de las 11 p. m. y el #18 (P3) a las 11:47 p. m. del sábado | Escribir las pruebas antes que el código: el Sprint cerró con 93 pruebas (14 de la P1, 9 de la P2 y 13 de la P3) |
| Arrancar cada tarea un día antes de su fecha límite, sobre todo si otra depende de ella | Dejar las dailies y el Burndown para el final: es la tercera retro en que queda pendiente | Aprobar el PR antes del merge: el #15, el #17 y el #18 tuvieron revisión y no hubo commits directos a `main` |
| Reportar la daily en el grupo antes de las 9 p. m. del mismo día, para que Michelle la registre esa noche | Encadenar las tareas sin margen: la P2 atrasó la P3 y la P3 atrasó la Release | Separar en el CI las pruebas unitarias de las de punta a punta, para ver rápido qué se rompió |
| | | Revisar en menos de 24 h: el #18 se abrió el sábado a las 11:47 p. m. y se fusionó el domingo a las 2:00 p. m. |

**Lecciones aprendidas:**

1. En un Sprint con tareas encadenadas, el atraso de una se pasa a todas las siguientes.
2. La acción de registrar el Burndown cada noche no se ha cumplido en tres Sprints, aunque tiene responsable desde el Sprint 1: depende de que todo el equipo reporte a tiempo, por eso se fija una hora límite diaria.
3. La regla de "revisar antes del merge" del Sprint 2 sí se cumplió en todos los PR del Sprint 3.

