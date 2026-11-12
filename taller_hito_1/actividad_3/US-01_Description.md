# US-01. Enviar el mensaje y ver la decisión

## Enunciado

Como cliente de Banco Andino, quiero escribir mi caso en texto libre y enviarlo desde una pantalla con un campo y un botón, para recibir en la misma interacción qué entendió el banco y qué va a pasar con mi solicitud.

## Valor de negocio

El cliente llega al canal con un problema ya formulado en sus palabras. Esta historia le evita elegir un tipo de trámite o completar un formulario previo. El banco gana una primera atención consistente: la persona comprueba la lectura y ve, en la misma pantalla, si el caso quedó remitido, si debe aclarar datos o si un operador continúa la atención.

US-01 es la cara del MVP. Las historias siguientes producen la intención, los datos, el resumen y la acción. Esta historia se da por cumplida cuando esa decisión se puede escribir y leer en el canal.

## Actor

Cliente del banco, en la pantalla de solicitud. El inicio de sesión queda fuera de esta historia. La pantalla asume que la persona ya está frente al campo de texto.

## Alcance

Incluye:

- Una pantalla con un campo de texto libre y un botón para enviar la solicitud.
- El envío del texto escrito y la espera en la misma pantalla.
- La presentación de la decisión: resumen, intención, confianza, datos encontrados, datos faltantes, acción y motivo.
- Un estado visible, y solo uno: remitida, incompleta o derivada.

No incluye:

- El contrato HTTP, la persistencia y el código de estado. Eso corresponde a US-02 y US-10.
- La clasificación, la extracción, el resumen y la elección de la acción. Eso corresponde a US-03 a US-06.
- La autenticación, la resolución del trámite y la conversación del operador con el cliente.

## Recorrido en pantalla

1. El cliente abre la pantalla de solicitud. Ve el campo de texto libre y el botón de envío. No hay menú de trámites ni campos de caso, monto o fecha.
2. Redacta el caso con sus palabras y envía.
3. La pantalla permanece en el mismo lugar mientras espera la respuesta. El botón no admite un segundo envío hasta que llegue la decisión.
4. Al llegar la respuesta, la pantalla muestra la lectura del banco y el estado resultante.
5. El cliente comprueba el resumen y entiende el siguiente paso sin salir del canal.

## Qué debe ver el cliente

La respuesta se presenta en lenguaje de negocio. Los códigos internos pueden acompañar la decisión, pero el estado visible usa estas tres etiquetas.

| Estado visible | Cuándo aparece | Qué comunica la pantalla |
| --- | --- | --- |
| Remitida | La acción es remitir el caso | El banco entendió una devolución pendiente y la solicitud pasó al proceso que la resuelve. Muestra resumen, intención y motivo. |
| Incompleta | La acción es pedir aclaración | La intención se sostiene y faltan datos. Muestra el resumen y las preguntas concretas, sin pedir que repita el relato. |
| Derivada | La acción es derivar a un operador | Hay más de una lectura o la confianza es baja. Muestra el resumen y el motivo, e informa que un operador continúa la atención. |

En los tres estados la pantalla muestra, además, la confianza, los datos encontrados y los datos que faltan. Si no falta ningún dato, esa sección se muestra vacía.

## Caso de referencia en el canal

El relato base es «Llevo varios días esperando la devolución de mi dinero».

| Mensaje que escribe el cliente | Estado que ve |
| --- | --- |
| «Llevo varios días esperando la devolución de mi dinero.» | Incompleta. La pantalla pide número de caso, monto y fecha. |
| «Llevo varios días esperando la devolución de mi dinero del caso 45821, por $120.000, de la compra del 3 de noviembre.» | Remitida. La pantalla muestra el resumen actualizado y que la solicitud fue remitida. |
| «Llevo varios días esperando la devolución de mi dinero, o quizá fue un cobro de la tarjeta que no reconozco.» | Derivada. La pantalla avisa que un operador continúa la atención. |

## Criterios de aceptación

1. Dado un cliente en la pantalla de solicitud, cuando observa el formulario, entonces ve un único campo de texto libre y un botón de envío, sin selector de trámite ni campos previos de caso, monto o fecha.
2. Dado un campo vacío, cuando intenta enviar, entonces la pantalla no dispara la solicitud y mantiene el campo listo para escribir.
3. Dado un texto escrito, cuando envía, entonces la interfaz manda ese texto y el cliente espera la respuesta en la misma pantalla.
4. Dado un envío en curso, cuando aún no llega la decisión, entonces no puede lanzar otro envío sobre la misma espera.
5. Dada la respuesta del motor, cuando la pantalla la presenta, entonces muestra resumen, intención, confianza, datos encontrados, datos faltantes, acción y motivo.
6. Dada una acción de remitir, cuando se muestra el resultado, entonces el estado visible es remitida y no aparecen preguntas de aclaración.
7. Dada una acción de pedir aclaración, cuando se muestra el resultado, entonces el estado visible es incompleta y se listan las preguntas concretas devueltas por el motor.
8. Dada una acción de derivar, cuando se muestra el resultado, entonces el estado visible es derivada, se informa que un operador continúa y no se pide al cliente que vuelva a contar el caso.
9. Dada cualquiera de las tres respuestas, cuando termina la interacción, entonces la pantalla muestra un solo estado.

## Dependencias

- US-02 entrega el cuerpo de la decisión que esta pantalla proyecta.
- US-07, US-08 y US-09 fijan el contenido de negocio de cada estado para el caso de referencia.

## Definición de terminado

La historia está terminada cuando un cliente puede escribir uno de los tres mensajes de referencia, enviarlo una vez y leer en la misma pantalla el estado que le corresponde, con el resumen y el resto de la decisión visibles.
