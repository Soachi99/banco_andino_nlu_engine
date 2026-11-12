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

## Actividad 3 — Trabajando como Tech Lead con GenAI

En esta actividad el trabajo de las dos anteriores se consolida en una especificación de requerimientos del software (ERS), versión 1.0, del 12 de noviembre de 2026. El documento fija qué debe hacer el motor, qué recibe el cliente, cómo se recorre un caso, qué decisión sale de cada mensaje y con qué modelo, contratos y arquitectura se sostiene esa decisión. El ejercicio de Uber queda fuera de este sistema.

El mismo texto está en Word y en PDF:

| Archivo | Contenido |
| --- | --- |
| [`especificacion_requerimientos_motor_nlu.docx`](taller_hito_1/especificacion_requerimientos_motor_nlu.docx) | Especificación en Word |
| [`especificacion_requerimientos_motor_nlu.pdf`](taller_hito_1/especificacion_requerimientos_motor_nlu.pdf) | La misma especificación en PDF |

Cada capítulo sale de un artefacto ya construido:

1. Propósito y alcance del identificador: termina cuando el mensaje ya tiene una decisión.
2. Actores y fronteras: visitante, cliente logueado, proceso de negocio y operador.
3. Funcionalidades, beneficios y recorrido del cliente (Actividad 2, prompts 1 a 3).
4. Casos de uso y las tres salidas: remitir, pedir aclaración o derivar (Actividad 2 y `casos_de_uso`).
5. Requisitos funcionales y reglas de negocio.
6. Contratos de la respuesta HTTP y la equivalencia de nombres.
7. Modelo de datos: `Request`, `Interpretation` y `Decision` (Actividad 2, prompt 6).
8. Interacción de identidades (Actividad 1, proyecto NLU).
9. Secuencia de la identificación (Actividad 1, proyecto NLU).
10. Arquitectura de despliegue: la vista tentativa en AWS y la de microservicios, cada uno con su base.
11. Correspondencia de cada capítulo con el artefacto del taller del que proviene.

Un mismo ejemplo recorre toda la especificación: «Llevo varios días esperando la devolución de mi dinero». Con solo ese texto el motor pide número de caso, monto y fecha. Si el relato trae esos datos, el caso se remite. Si además admite un cobro de tarjeta no reconocido, pasa a un operador.

### Backlog del MVP

A partir de esa especificación se armó el backlog del identificador. El corte del MVP es un mensaje en texto libre que, en un solo `POST /api/solicitudes`, devuelve una decisión persistida y visible: intención, confianza, datos encontrados, datos faltantes, resumen, una sola acción y su motivo. La acción es remitir el caso, pedir una aclaración o derivar a un operador.

El trabajo quedó en tres documentos encadenados:

| Documento | Qué contiene |
| --- | --- |
| [`UserHistories.md`](taller_hito_1/actividad_3/UserHistories.md) | Las once historias del MVP, de la pantalla al recorrido del coordinador. |
| [`US-01_Description.md`](taller_hito_1/actividad_3/US-01_Description.md) | La primera historia, descrita como Product Owner: el cliente escribe en texto libre y ve la decisión en la misma pantalla. |
| [`US-01_Work_items.md`](taller_hito_1/actividad_3/US-01_Work_items.md) | Los tickets de esa historia: modelo de presentación, captura, envío, panel de los tres estados y verificación del caso de referencia. |

[`UserHistories.md`](taller_hito_1/actividad_3/UserHistories.md) fija el alcance. [`US-01_Description.md`](taller_hito_1/actividad_3/US-01_Description.md) abre la primera historia, que es la cara del canal. [`US-01_Work_items.md`](taller_hito_1/actividad_3/US-01_Work_items.md) la parte en trabajo de implementación. La pantalla React solo habla con la API; el motor, la persistencia y la autenticación quedan en las historias siguientes.

**En este taller se trabaja el primer ticket de esa primera historia: [US01-01. Modelo de presentación de la decisión](taller_hito_1/actividad_3/US-01_Work_items.md).** Define cómo la pantalla traduce la respuesta del motor al lenguaje del cliente: Remitida, Incompleta o Derivada, con resumen, intención, confianza, datos encontrados, datos faltantes, acción y motivo. Los demás tickets de US-01 consumen ese modelo.
