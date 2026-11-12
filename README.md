# Hito 1 — Parte 2

Taller de la asignatura **IA en Negocios Digitales**.

## Proyecto — Identificación de solicitudes en lenguaje natural

Este repositorio desarrolla el motor NLU de Banco Andino. El sistema interpreta el mensaje del cliente, reconoce la intención principal, extrae la información relevante, resume el problema y señala ambigüedades o datos insuficientes. Según ese resultado, remite el caso al siguiente proceso, pide una aclaración o lo deriva a un operador.

Los diagramas de ese proceso están en [`taller_hito_1/actividad_1/proyecto_nlu`](taller_hito_1/actividad_1/proyecto_nlu):

| Archivo | Contenido |
| --- | --- |
| [`diagrama_secuencia.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md) | Secuencia: orden en el tiempo, participantes y puntos clave |
| [`secuencia_identificacion_solicitudes.puml`](taller_hito_1/actividad_1/proyecto_nlu/secuencia_identificacion_solicitudes.puml) | Fuente PlantUML de la secuencia |
| [`secuencia_identificacion_solicitudes.png`](taller_hito_1/actividad_1/proyecto_nlu/secuencia_identificacion_solicitudes.png) | Gráfica de la secuencia |
| [`diagrama_interaccion_identidades.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_interaccion_identidades.md) | Identidades y vínculos permitidos entre ellas |
| [`interaccion_identidades.puml`](taller_hito_1/actividad_1/proyecto_nlu/interaccion_identidades.puml) | Fuente PlantUML de la interacción de identidades |
| [`interaccion_identidades.png`](taller_hito_1/actividad_1/proyecto_nlu/interaccion_identidades.png) | Gráfica de la interacción de identidades |
| [`arquitectura_aws.md`](taller_hito_1/actividad_1/proyecto_nlu/arquitectura_aws.md) | Arquitectura AWS tentativa y criterios de despliegue |
| [`arquitectura_aws.py`](taller_hito_1/actividad_1/proyecto_nlu/arquitectura_aws.py) | Script Diagrams de esa arquitectura |
| [`arquitectura_nlu_aws.png`](taller_hito_1/actividad_1/proyecto_nlu/arquitectura_nlu_aws.png) | Gráfica de la arquitectura AWS |

La secuencia ordena el flujo que el repo va a implementar (React en el canal y Node en la API y los agentes). La interacción de identidades fija quién puede hablar con quién. La arquitectura AWS tentativa muestra cómo se desplegaría ese mismo flujo. Los tres responden a la Actividad 1, en la parte de construir diagramas con GenAI, y quedan como referencia del proyecto.

## Actividad 1 — Construyendo diagramas con GenAI

Las respuestas de la **Actividad 1** sobre la aplicación de transporte están en [`taller_hito_1/actividad_1/uber`](taller_hito_1/actividad_1/uber).

El diagrama de secuencia del proyecto está explicado en [`taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md). El de interacción de identidades, en [`taller_hito_1/actividad_1/proyecto_nlu/diagrama_interaccion_identidades.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_interaccion_identidades.md). La arquitectura AWS tentativa, en [`taller_hito_1/actividad_1/proyecto_nlu/arquitectura_aws.md`](taller_hito_1/actividad_1/proyecto_nlu/arquitectura_aws.md). Forman parte de esta actividad y, a la vez, describen el flujo que el repositorio va a desarrollar.

El documento principal es [`taller_hito_1/actividad_1/uber/actividad_1_respuestas.md`](taller_hito_1/actividad_1/uber/actividad_1_respuestas.md). Ahí quedan los tres prompts del taller, las salidas de ChatGPT y Claude, y la comparación entre ambas:

1. Diagrama de secuencia en PlantUML de una aplicación de transporte.
2. Gráfica de ese diagrama.
3. Diagrama de arquitectura en AWS con la librería Diagrams (Python).

En la misma carpeta están los artefactos que el documento cita:

| Archivo | Contenido |
| --- | --- |
| [`architecture_chatgpt.py`](taller_hito_1/actividad_1/uber/architecture_chatgpt.py) | Script de arquitectura AWS generado por ChatGPT |
| [`architecture_claude.py`](taller_hito_1/actividad_1/uber/architecture_claude.py) | Script de arquitectura AWS generado por Claude |
| [`diagrama chatgpt.jpg`](taller_hito_1/actividad_1/uber/diagrama%20chatgpt.jpg) | Diagrama de secuencia de ChatGPT |
| [`diagrama claude.png`](taller_hito_1/actividad_1/uber/diagrama%20claude.png) | Diagrama de secuencia de Claude |
| [`uber_aws_architecture_chatgpt.png`](taller_hito_1/actividad_1/uber/uber_aws_architecture_chatgpt.png) | Arquitectura AWS obtenida del script de ChatGPT |
| [`uber_aws_architecture_claude.png`](taller_hito_1/actividad_1/uber/uber_aws_architecture_claude.png) | Arquitectura AWS obtenida del script de Claude |
