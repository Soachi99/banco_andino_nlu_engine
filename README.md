# Hito 1 — Parte 2

Taller de la asignatura **IA en Negocios Digitales**.

El orden del taller es este: primero el ejercicio de la aplicación de transporte (Uber), para practicar los diagramas con GenAI. Después va lo que corresponde al proyecto que hay que construir como MVP, el identificador de solicitudes de Banco Andino.

## Actividad 1 — Construyendo diagramas con GenAI

Dentro de esta actividad se hizo primero Uber y, a continuación, los diagramas del motor.

### 1. Aplicación de transporte (Uber)

Las respuestas sobre la aplicación de transporte están en [`taller_hito_1/actividad_1/uber`](taller_hito_1/actividad_1/uber).

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

### 2. Proyecto — Identificación de solicitudes en lenguaje natural

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

La secuencia ordena el flujo que el repo va a implementar (React en el canal y Node en la API y los agentes). La interacción de identidades fija quién puede hablar con quién. La arquitectura AWS tentativa muestra cómo se desplegaría ese mismo flujo. Estos diagramas quedan como referencia del MVP.

## Actividad 2 — Planeando un software con GenAI

A partir de aquí el trabajo es el MVP del motor, ya no el ejercicio de Uber.

Las respuestas están en [`taller_hito_1/actividad_2/respuestas_actividad_2.md`](taller_hito_1/actividad_2/respuestas_actividad_2.md). Planifican el identificador: qué hace el motor, qué gana el cliente, cómo recorre el caso y con qué modelo y arquitectura se sostiene.

1. Funcionalidades del motor, de mayor a menor prioridad.
2. Beneficios para el cliente.
3. Recorrido del cliente, del mensaje a la decisión.
4. Casos de uso del MVP y las tres salidas: remitir, pedir aclaración o derivar.
5. Modelo de datos: `Request`, `Interpretation` y `Decision`, con su diagrama entidad-relación.
6. Arquitectura de microservicios en AWS: frontend por la API, una base por servicio, CloudFront y balanceador.

El diagrama de casos de uso distingue al visitante del cliente logueado, y deja fuera del sistema al proceso de negocio y al operador:

| Archivo | Contenido |
| --- | --- |
| [`casos_de_uso.puml`](taller_hito_1/actividad_2/casos_de_uso.puml) | Fuente PlantUML de los casos de uso |
| [`casos_de_uso.png`](taller_hito_1/actividad_2/casos_de_uso.png) | Gráfica de esos casos de uso |
