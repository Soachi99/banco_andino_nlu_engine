# Work items — US-01. Enviar el mensaje y ver la decisión

Historia padre: [US-01_Description.md](US-01_Description.md).

El canal es una pantalla React. Habla solo con `POST /api/solicitudes` y proyecta la decisión que devuelve US-02. Estos tickets no construyen el motor, la persistencia, la autenticación ni la atención del operador.

Esfuerzo total estimado: 22 horas.

## US01-01. Modelo de presentación de la decisión

- **ID del Ticket:** US01-01
- **Título del Ticket:** Definir el modelo de presentación que traduce la decisión del motor al lenguaje de la pantalla
- **Descripción:** La interfaz necesita un contrato de vista propio, separado del cuerpo HTTP. Este ticket fija los campos que la pantalla puede mostrar y la correspondencia entre la acción del motor y el estado visible: remitida, incompleta o derivada. El resto de los tickets de US-01 consume este modelo y no interpreta códigos de negocio por su cuenta.
- **Criterios de aceptación:**
  - El modelo de vista incluye resumen, intención, confianza, datos encontrados, datos faltantes, acción, motivo y, solo si la acción es `SOLICITAR_INFORMACION`, la lista de preguntas.
  - `REMITIR_PROCESO` se proyecta como estado visible Remitida y estado de respuesta `REMITIDA`.
  - `SOLICITAR_INFORMACION` se proyecta como estado visible Incompleta y estado de respuesta `INCOMPLETA`.
  - `DERIVAR_OPERADOR` se proyecta como estado visible Derivada y estado de respuesta `DERIVADA`.
  - Una respuesta con acción distinta de `SOLICITAR_INFORMACION` llega a la vista sin preguntas.
  - Una respuesta sin datos faltantes llega a la vista con esa colección vacía.
- **Prioridad:** Alta
- **Estimación de esfuerzo (en horas):** 3
- **Tareas Técnicas:**
  - Declarar el tipo de la respuesta de `POST /api/solicitudes` con `estado`, `intencion.tipo`, `confianza`, datos encontrados, datos faltantes, `resumen`, `accion`, `motivo` y `preguntas` opcional.
  - Declarar el modelo de vista con las tres etiquetas visibles: Remitida, Incompleta y Derivada.
  - Implementar la función de proyección de acción y estado hacia esa etiqueta.
  - Cubrir la proyección con pruebas unitarias de las tres acciones y del caso sin datos faltantes.
- **Notas:** US-02 es la fuente del cuerpo. Si el endpoint aún no existe, este ticket igual puede cerrarse contra un fixture con la forma acordada. La pantalla no conoce a los agentes ni abre la base.

## US01-02. Pantalla de captura en texto libre

- **ID del Ticket:** US01-02
- **Título del Ticket:** Construir la pantalla con un campo de texto libre y un botón de envío
- **Descripción:** El cliente entra a la pantalla de solicitud y redacta el caso con sus palabras. La captura se limita a un campo y un botón. No hay selector de trámite ni campos previos de caso, monto o fecha. Un envío vacío no sale del canal.
- **Criterios de aceptación:**
  - Al abrir la pantalla se ve un único campo de texto libre y un botón de envío.
  - No hay menú de trámites ni campos de número de caso, monto o fecha antes del envío.
  - Con el campo vacío, o con solo espacios, el envío no dispara la solicitud y el campo sigue editable.
  - Con texto escrito, el botón queda habilitado para enviar.
- **Prioridad:** Alta
- **Estimación de esfuerzo (en horas):** 4
- **Tareas Técnicas:**
  - Crear la vista React de la solicitud y su estado local del texto.
  - Renderizar un área de texto y un botón, sin controles de formulario de trámite.
  - Validar en cliente que el texto, ya recortado, no esté vacío antes de continuar el flujo.
  - Añadir una prueba de componente para el estado inicial y para el bloqueo del envío vacío.
- **Notas:** El inicio de sesión queda fuera. La ruta puede asumir que el cliente ya está frente a esta pantalla. El envío real y la espera se implementan en US01-03.

## US01-03. Envío del mensaje y espera en la misma pantalla

- **ID del Ticket:** US01-03
- **Título del Ticket:** Enviar el texto a la API y bloquear un segundo envío mientras llega la decisión
- **Descripción:** Al confirmar el texto, la interfaz llama a `POST /api/solicitudes` y el cliente permanece en la misma pantalla hasta recibir la decisión. Durante esa espera no puede lanzar otra solicitud. Al terminar, el resultado queda listo para el panel de US01-04.
- **Criterios de aceptación:**
  - Un texto válido se envía en el cuerpo de `POST /api/solicitudes` como el mensaje redactado.
  - La pantalla no navega a otra ruta mientras espera.
  - Con el envío en curso, el botón no admite otro envío.
  - Si la llamada falla, la pantalla informa el error, conserva el texto y vuelve a habilitar el envío.
  - Si la llamada responde, el texto enviado y la decisión proyectada quedan disponibles para mostrarse en la misma vista.
- **Prioridad:** Alta
- **Estimación de esfuerzo (en horas):** 5
- **Tareas Técnicas:**
  - Implementar el cliente HTTP del canal, único punto de salida hacia la API.
  - Modelar los estados de interfaz: edición, enviando, respondida y error.
  - Deshabilitar el control de envío mientras el estado sea enviando.
  - Normalizar la respuesta con la proyección de US01-01 antes de entregarla a la vista.
  - Probar el bloqueo del doble envío y la recuperación ante un error de red con el cliente simulado.
- **Notas:** La interfaz solo habla con la API. Un adaptador o mock de US-02 basta para cerrar este ticket. El código HTTP y la persistencia no se implementan aquí.

## US01-04. Panel de la decisión y sus tres estados

- **ID del Ticket:** US01-04
- **Título del Ticket:** Mostrar la decisión en un solo estado visible: Remitida, Incompleta o Derivada
- **Descripción:** Cuando la API responde, la misma pantalla presenta la lectura del banco. El cliente ve el resumen, la intención, la confianza, los datos encontrados, los datos faltantes, la acción y el motivo. El estado visible es uno solo y el mensaje de cierre cambia según la acción.
- **Criterios de aceptación:**
  - La decisión muestra resumen, intención, confianza, datos encontrados, datos faltantes, acción y motivo.
  - Si no hay datos faltantes, esa sección se muestra vacía.
  - Con `REMITIR_PROCESO`, el estado visible es Remitida, se comunica que la solicitud pasó al proceso que la resuelve y no aparecen preguntas.
  - Con `SOLICITAR_INFORMACION`, el estado visible es Incompleta y se listan las preguntas devueltas, sin pedir que el cliente repita el relato.
  - Con `DERIVAR_OPERADOR`, el estado visible es Derivada, se muestra el motivo y se informa que un operador continúa la atención.
  - Las tres respuestas no pueden mostrar más de un estado visible a la vez.
- **Prioridad:** Alta
- **Estimación de esfuerzo (en horas):** 6
- **Tareas Técnicas:**
  - Crear el panel de decisión y componerlo en la pantalla de US01-02 después de una respuesta exitosa.
  - Renderizar las secciones comunes desde el modelo de vista de US01-01.
  - Implementar el bloque de Remitida sin lista de preguntas.
  - Implementar el bloque de Incompleta con la lista de preguntas concretas.
  - Implementar el bloque de Derivada con el aviso de continuidad por un operador.
  - Añadir pruebas de componente con un fixture por cada acción y uno con datos faltantes vacíos.
- **Notas:** Las etiquetas visibles son Remitida, Incompleta y Derivada. Los códigos `REMITIR_PROCESO`, `SOLICITAR_INFORMACION` y `DERIVAR_OPERADOR` pueden acompañar la acción, siempre debajo de ese lenguaje de negocio.

## US01-05. Verificación del caso de referencia en el canal

- **ID del Ticket:** US01-05
- **Título del Ticket:** Verificar en la pantalla los tres mensajes de referencia de la devolución
- **Descripción:** US-01 queda terminada cuando el cliente escribe cada mensaje de referencia, lo envía una vez y lee en la misma pantalla el estado que le corresponde, con el resumen y el resto de la decisión. Este ticket recorre ese criterio de punta a punta sobre el canal.
- **Criterios de aceptación:**
  - «Llevo varios días esperando la devolución de mi dinero.» termina en Incompleta y la pantalla pide número de caso, monto y fecha.
  - «Llevo varios días esperando la devolución de mi dinero del caso 45821, por $120.000, de la compra del 3 de noviembre.» termina en Remitida, con el resumen y sin preguntas.
  - «Llevo varios días esperando la devolución de mi dinero, o quizá fue un cobro de la tarjeta que no reconozco.» termina en Derivada y avisa que un operador continúa la atención.
  - En los tres recorridos hay un solo envío y un solo estado visible.
  - El campo vacío sigue sin disparar la solicitud.
- **Prioridad:** Media
- **Estimación de esfuerzo (en horas):** 4
- **Tareas Técnicas:**
  - Preparar tres fixtures de respuesta alineados con US-02, US-07, US-08 y US-09.
  - Automatizar el recorrido de cada mensaje: escribir, enviar una vez y afirmar el estado, el resumen y la presencia o ausencia de preguntas.
  - Automatizar el intento de envío con el campo vacío.
  - Dejar el guion manual de los tres mensajes para la demostración del MVP.
- **Notas:** Si el motor de US-03 a US-09 aún no está integrado, la verificación usa los fixtures. Al conectar el `POST` real, el mismo guion sirve para la prueba de aceptación sin cambiar la pantalla. La resolución del trámite y la conversación del operador quedan fuera del recorrido.
