export const ACCIONES = ["REMITIR_PROCESO", "SOLICITAR_INFORMACION", "DERIVAR_OPERADOR"] as const

export type Accion = (typeof ACCIONES)[number]

export const ESTADOS_RESPUESTA = ["REMITIDA", "INCOMPLETA", "DERIVADA"] as const

export type EstadoRespuesta = (typeof ESTADOS_RESPUESTA)[number]

type Lectura = {
  readonly intencion: { readonly tipo: string }
  readonly confianza: number
  readonly datosEncontrados: readonly string[]
  readonly datosFaltantes: readonly string[]
  readonly resumen: string
  readonly motivo: string
}

export type RespuestaRemitir = Lectura & {
  readonly estado: "REMITIDA"
  readonly accion: "REMITIR_PROCESO"
}

export type RespuestaSolicitarInformacion = Lectura & {
  readonly estado: "INCOMPLETA"
  readonly accion: "SOLICITAR_INFORMACION"
  readonly preguntas: readonly string[]
}

export type RespuestaDerivar = Lectura & {
  readonly estado: "DERIVADA"
  readonly accion: "DERIVAR_OPERADOR"
}

export type RespuestaSolicitud = RespuestaRemitir | RespuestaSolicitarInformacion | RespuestaDerivar
