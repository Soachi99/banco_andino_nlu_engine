import type {
  RespuestaDerivar,
  RespuestaRemitir,
  RespuestaSolicitarInformacion,
} from "../../contract/respuesta-solicitud"

export const fixtureRemitir = {
  estado: "REMITIDA",
  accion: "REMITIR_PROCESO",
  intencion: { tipo: "devolución pendiente" },
  confianza: 0.92,
  datosEncontrados: ["caso 45821", "$120.000", "3 de noviembre"],
  datosFaltantes: [],
  resumen:
    "El cliente espera la devolución de $120.000 del caso 45821, de la compra del 3 de noviembre.",
  motivo: "La intención es única, la confianza alcanza y están el caso, el monto y la fecha.",
} satisfies RespuestaRemitir

export const fixtureSolicitarInformacion = {
  estado: "INCOMPLETA",
  accion: "SOLICITAR_INFORMACION",
  intencion: { tipo: "devolución pendiente" },
  confianza: 0.88,
  datosEncontrados: ["devolución", "dinero"],
  datosFaltantes: ["número de caso", "monto", "fecha"],
  resumen: "El dinero no ha vuelto tras varios días.",
  motivo: "La intención es clara y el cliente puede aportar número de caso, monto y fecha.",
  preguntas: [
    "¿Cuál es el número de caso?",
    "¿Cuál es el monto?",
    "¿Cuál es la fecha de la compra?",
  ],
} satisfies RespuestaSolicitarInformacion

export const fixtureDerivar = {
  estado: "DERIVADA",
  accion: "DERIVAR_OPERADOR",
  intencion: { tipo: "devolución pendiente" },
  confianza: 0.41,
  datosEncontrados: ["devolución", "cobro de tarjeta"],
  datosFaltantes: ["número de caso", "monto", "fecha"],
  resumen: "El cliente espera una devolución, o quizá un cobro de la tarjeta que no reconoce.",
  motivo: "El mensaje admite más de una lectura: devolución pendiente y transacción no reconocida.",
} satisfies RespuestaDerivar

export const fixtureSinDatosFaltantes = {
  estado: "DERIVADA",
  accion: "DERIVAR_OPERADOR",
  intencion: { tipo: "devolución pendiente" },
  confianza: 0.37,
  datosEncontrados: ["devolución", "cobro de tarjeta"],
  datosFaltantes: [],
  resumen: "Hay dos lecturas posibles y no queda un dato por pedir.",
  motivo: "La confianza es baja y el caso pasa a un operador.",
} satisfies RespuestaDerivar
