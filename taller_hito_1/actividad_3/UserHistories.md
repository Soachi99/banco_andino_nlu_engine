# Historias de usuario — MVP del identificador de solicitudes

El MVP del identificador de solicitudes de Banco Andino habilita al cliente para describir su caso en texto libre y obtener, en la misma interacción, una decisión de negocio lista para operar. El canal entrega el mensaje en un único `POST /api/solicitudes`. Esa llamada persiste la solicitud, la interpretación y la decisión, y devuelve al cliente la intención principal, la confianza, los datos encontrados, los datos faltantes, un resumen breve, la acción elegida y el motivo.

La decisión cierra el caso en una de tres acciones comerciales: `REMITIR_PROCESO`, cuando la intención es única, la confianza es suficiente y constan número de caso, monto y fecha; `SOLICITAR_INFORMACION`, cuando la intención se sostiene y falta alguno de esos datos, con las preguntas concretas; o `DERIVAR_OPERADOR`, cuando el mensaje admite más de una lectura o la confianza es baja. El caso de referencia es «Llevo varios días esperando la devolución de mi dinero»: sin caso, monto ni fecha solicita esos tres datos; con el caso 45821, $120.000 y la compra del 3 de noviembre remite la devolución pendiente; si además admite un cobro de tarjeta no reconocido, deriva el caso.

Este MVP solo cubre la identificación y el enrutamiento de la solicitud. La autenticación de la sesión, la ejecución del trámite una vez remitido y la gestión del operador después de recibir el caso pertenecen a los procesos posteriores del banco.

## US-01. Enviar el mensaje y ver la decisión

Como cliente, quiero escribir mi caso en texto libre y enviarlo desde una pantalla con un campo y un botón, para recibir en la misma interacción qué entendió el banco y qué va a pasar.

- La pantalla no pide tipo de trámite ni formulario previo.
- Tras el envío, muestra el resumen, la intención, la confianza, los datos encontrados, los datos que faltan, la acción y el motivo.
- El estado visible es uno: remitida, incompleta o derivada.

## US-02. Recibir una sola decisión por mensaje

Como cliente, quiero que cada envío responda una sola vez con una decisión completa, para saber si el trámite sigue, si debo aclarar algo o si lo toma una persona.

- `POST /api/solicitudes` responde HTTP 200 en las tres salidas. El destino se distingue en el cuerpo, no en el código de estado.
- El cuerpo trae `estado`, `intencion.tipo`, `confianza`, datos encontrados, datos faltantes, `resumen`, `accion` y `motivo`.
- `accion` admite solo `REMITIR_PROCESO`, `SOLICITAR_INFORMACION` o `DERIVAR_OPERADOR`.
- `preguntas` aparece solo cuando la acción es `SOLICITAR_INFORMACION`.

## US-03. Reconocer la intención principal

Como motor, quiero clasificar la intención principal del texto y conservar la duda si otra lectura es igual de plausible, para que el caso tenga un destino.

- «Llevo varios días esperando la devolución de mi dinero» se clasifica como devolución pendiente.
- Si el texto también admite un cobro de tarjeta no reconocido, se conservan las dos lecturas.
- La intención va acompañada de una confianza: alta con una sola lectura clara; baja si el texto es vago o hay lecturas en competencia.

## US-04. Extraer lo que está y marcar lo que falta

Como motor, quiero obtener del texto las entidades y los identificadores, y marcar los atributos que el caso exige y no aparecen, para no pedir de nuevo lo que el cliente ya dijo.

- En una devolución pendiente, los datos mínimos son número de caso, monto y fecha. El producto se extrae solo si viene en el texto.
- Con «caso 45821, $120.000 y compra del 3 de noviembre», esos tres datos quedan como encontrados y no hay faltantes de remisión.
- Con el relato sin esos datos, faltan caso, monto y fecha.

## US-05. Resumir el problema y juzgar si alcanza

Como proceso de negocio y como operador, quiero un resumen de una o dos frases, las ambigüedades y un juicio de suficiencia, para trabajar sobre la lectura y no sobre el mensaje crudo.

- El resumen del ejemplo sin datos dice que el dinero no ha vuelto tras varios días.
- `suficiente` es falso si faltan caso, monto o fecha, o si hay más de una lectura.
- `suficiente` es verdadero solo con intención única, confianza suficiente y los tres datos mínimos.

## US-06. Elegir una sola acción y dejar el motivo

Como validador, quiero contrastar la lectura con las reglas del caso y elegir exactamente una acción con su motivo, para que clasificar, extraer o resumir no autoricen por sí solos el paso al siguiente proceso.

- Intención única, confianza suficiente y datos mínimos, con cliente logueado: `REMITIR_PROCESO`.
- Intención que se sostiene y falta un dato que el cliente puede aportar: `SOLICITAR_INFORMACION`, con las preguntas concretas.
- Más de una lectura o confianza baja: `DERIVAR_OPERADOR`, para visitante y logueado.
- El visitante no remite. La falta de identidad cuenta como dato faltante y la salida es pedir aclaración, salvo que el mensaje deba derivarse. El inicio de sesión queda fuera del identificador.

## US-07. Pedir solo lo que falta

Como cliente, quiero que, si mi intención es clara y faltan datos, me pregunten exactamente esos datos, para completar el caso sin repetir el relato.

- «Llevo varios días esperando la devolución de mi dinero» devuelve estado `INCOMPLETA`, acción `SOLICITAR_INFORMACION` y las preguntas de número de caso, monto y fecha.
- El motivo indica que la intención es clara y el cliente puede aportar esos tres datos.

## US-08. Remitir la devolución cuando el caso está completo

Como cliente logueado, quiero que mi devolución se remita al proceso de negocio cuando la intención es única, la confianza alcanza y están el caso, el monto y la fecha, para no repetir la historia en otro canal.

- «…devolución de mi dinero del caso 45821, por $120.000, de la compra del 3 de noviembre» devuelve estado `REMITIDA` y acción `REMITIR_PROCESO`.
- La respuesta incluye el resumen y la intención de devolución pendiente.
- El coordinador publica hacia el proceso de negocio y espera el acuse. La resolución del trámite queda fuera.

## US-09. Derivar cuando hay más de una lectura

Como cliente, quiero que un operador reciba el caso ya resumido cuando el mensaje admite más de una lectura o la confianza es baja, para no volver a contar lo sucedido.

- «…la devolución de mi dinero, o quizá fue un cobro de la tarjeta que no reconozco» devuelve estado `DERIVADA` y acción `DERIVAR_OPERADOR`.
- Compiten devolución pendiente y transacción no reconocida.
- La respuesta incluye el resumen y el motivo. El coordinador deja el caso para el operador y recibe el acuse. La atención posterior queda fuera.

## US-10. Dejar constancia de la solicitud, la lectura y la decisión

Como banco, quiero persistir la solicitud, la interpretación de ese mensaje y la decisión, para auditar la intención, los datos, el resumen, la confianza y el motivo.

- Cada `POST` crea una `Request` (`id`, `status`, `correlationId`, `createdAt`), una `Interpretation` y una sola `Decision`.
- `Request.status` proyecta la última decisión: `RECEIVED` al entrar, luego `INCOMPLETE`, `FORWARDED` o `ESCALATED`.
- La interpretación guarda `intentType`, `confidence`, `entities`, `identifiers`, `missingFields`, `summary`, `ambiguities` y `sufficient`.
- La decisión guarda `action`, `meetsRequirements`, `reason` y, solo si pide aclaración, `questions`.

## US-11. Recorrer el mensaje en el orden del motor

Como sistema, quiero que un solo coordinador integre la lectura y enrute el veredicto, para que cada mensaje termine en una de las tres salidas sin que los agentes se llamen entre sí.

- La interfaz solo habla con la API y la API solo llama a `analizar(mensaje)` en el coordinador.
- Intérprete y extractor corren a la vez sobre el texto crudo. El análisis contextual corre después, con el mensaje, la intención y los datos.
- El validador devuelve el veredicto. Solo el coordinador remite o deriva. Si la acción es pedir información, la respuesta vuelve por la misma llamada, sin otro servicio.
