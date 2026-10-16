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

**Lecciones aprendidas y plan de mejora (para la Demo, Producto C):**

1. Las tareas que dependen de otras se empiezan el primer día del Sprint, y el PR del que depende otra tarea se revisa de inmediato: la Tarea 7 quedó sin cerrar el jue 15 porque el PR #9 de la Tarea 6 se fusionó hasta el vie 16.
2. Los tests detectan errores de copia o edición: correr `pytest` después de cada cambio, incluso si solo se tocaron comentarios.
3. El modelo de mora marca al 85 % de los clientes y el F1 del churn es 0,296: revisar el umbral con el equipo de cobranza antes de la Demo.
4. Subir las evidencias (capturas, pairing, Trello) junto con el commit de cada tarea.
5. Registrar el Burndown cada noche (acción pendiente desde la Retrospectiva 1).