# Documentación del Corte 2 – FinTech Solutions × FinBank

| Carpeta | Contenido |
|---|---|
| `scrum/sprints.md` | Backlog de cada Sprint, puntos comprometidos/completados, Velocity y datos del Burndown |
| `scrum/dailies.md` | Bitácora de Daily Scrums |
| `scrum/retrospectivas.md` | Retrospectiva de cada Sprint (Start / Stop / Continue) |
| `xp/bitacora_xp.md` | Evidencia XP: pairing, PRs, ejecuciones de pytest, refactor antes/después |
| `evidencias/` | Fotos y capturas (pairing, pytest, PRs, Trello) |

## Flujo de trabajo (Integración continua y propiedad colectiva)

1. Nadie hace commit directo a `main`.
2. Cada tarea vive en una rama `feature/...` trabajada en pareja (piloto/copiloto).
3. Los commits de pareja llevan al final la línea `Co-authored-by:` del copiloto.
4. Se abre un Pull Request; lo revisa y aprueba el integrante que no estuvo en la pareja.
5. Solo con aprobación y tests en verde se hace merge a `main`.
