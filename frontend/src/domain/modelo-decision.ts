export const ESTADOS_VISIBLES = ["Remitida", "Incompleta", "Derivada"] as const

export type EstadoVisible = (typeof ESTADOS_VISIBLES)[number]

type LecturaVisible = {
  readonly resumen: string
  readonly intencion: string
  readonly confianza: number
  readonly datosEncontrados: readonly string[]
  readonly datosFaltantes: readonly string[]
  readonly motivo: string
}

export type DecisionRemitida = LecturaVisible & {
  readonly estadoVisible: "Remitida"
  readonly estado: "REMITIDA"
  readonly accion: "REMITIR_PROCESO"
}

export type DecisionIncompleta = LecturaVisible & {
  readonly estadoVisible: "Incompleta"
  readonly estado: "INCOMPLETA"
  readonly accion: "SOLICITAR_INFORMACION"
  readonly preguntas: readonly string[]
}

export type DecisionDerivada = LecturaVisible & {
  readonly estadoVisible: "Derivada"
  readonly estado: "DERIVADA"
  readonly accion: "DERIVAR_OPERADOR"
}

export type ModeloDecision = DecisionRemitida | DecisionIncompleta | DecisionDerivada
