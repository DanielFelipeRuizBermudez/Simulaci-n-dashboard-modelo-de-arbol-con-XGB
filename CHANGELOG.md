# Changelog

Cambios de cada versión del dashboard de analítica predictiva de FinTech Solutions para FinBank S.A.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.0] – 2026-11-15 · Sprint 3: Despliegue y validación

### Agregado
- Cola de llamadas de Sol en la pestaña Morosidad, ordenada por riesgo × exposición (PR #15).
- Protocolo de Sol: verificación de identidad con dos datos y escalamiento a asesor humano (PR #15).
- Herramienta `get_call_queue` para que Sol responda a quién llamar primero (PR #15).
- Pruebas de punta a punta (datos → validación → modelo → alertas → cola de Sol) y prueba de humo de la app (PR #17).
- CI en dos pasos: pruebas unitarias y pruebas de punta a punta (PR #17).
- Pestaña Monitoreo con PSI por variable, semáforo y simulación de un lote desplazado (PR #18).
- README con enlace público, manual de uso y alcance de Sol; este CHANGELOG (PR #16).

### Cambiado
- Versión mínima de Streamlit: 1.40, la primera que trae `st.segmented_control` (PR #15).

## [0.2] – 2026-10-16 · Sprint 2: Modelos y dashboards

### Agregado
- Reportes de validación y documentación de los modelos de mora y churn (PR #6, #7).
- Dashboard de mora con alertas por nivel y prioridad por riesgo × exposición (PR #9).
- Dashboard de churn con prioridad por valor del cliente y variable SHAP de cada alerta (PR #10).
- 57 pruebas automatizadas en GitHub Actions.

## [0.1] – 2026-10-14 · Sprint 1: Calidad de datos

### Agregado
- Estructura del proyecto y CI con GitHub Actions (PR #1).
- Ingesta de datos documentada (PR #2).
- Reglas de validación y limpieza para mora y churn, probadas con TDD (PR #3, #4).
