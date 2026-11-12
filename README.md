# Hito 1 — Parte 2

Taller de la asignatura **IA en Negocios Digitales**.

## Proyecto — Identificación de solicitudes en lenguaje natural

Este repositorio desarrolla el motor NLU de Banco Andino. El sistema interpreta el mensaje del cliente, reconoce la intención principal, extrae la información relevante, resume el problema y señala ambigüedades o datos insuficientes. Según ese resultado, remite el caso al siguiente proceso, pide una aclaración o lo deriva a un operador.

El diagrama de secuencia de ese proceso está en [`taller_hito_1/actividad_1/proyecto_nlu`](taller_hito_1/actividad_1/proyecto_nlu):

| Archivo | Contenido |
| --- | --- |
| [`diagrama_secuencia.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md) | Explicación del flujo, participantes y puntos clave |
| [`secuencia_identificacion_solicitudes.puml`](taller_hito_1/actividad_1/proyecto_nlu/secuencia_identificacion_solicitudes.puml) | Fuente PlantUML |
| [`secuencia_identificacion_solicitudes.png`](taller_hito_1/actividad_1/proyecto_nlu/secuencia_identificacion_solicitudes.png) | Gráfica del diagrama |

Ese diagrama es la referencia del flujo que el repo va a implementar (React en el canal y Node en la API y los agentes). También responde a la Actividad 1, en la parte de construir diagramas con GenAI.

## Actividad 1 — Construyendo diagramas con GenAI

Las respuestas de la **Actividad 1** sobre la aplicación de transporte están en [`taller_hito_1/actividad_1/uber`](taller_hito_1/actividad_1/uber).

El diagrama de secuencia del proyecto —identificación de solicitudes— está explicado en [`taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md`](taller_hito_1/actividad_1/proyecto_nlu/diagrama_secuencia.md). Forma parte de esta actividad y, a la vez, es el flujo que el repositorio va a desarrollar.

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
