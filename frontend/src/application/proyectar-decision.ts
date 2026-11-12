import type {
  RespuestaDerivar,
  RespuestaSolicitarInformacion,
  RespuestaRemitir,
  RespuestaSolicitud,
} from "../contract/respuesta-solicitud"
import type {
  DecisionDerivada,
  DecisionIncompleta,
  DecisionRemitida,
  ModeloDecision,
} from "../domain/modelo-decision"

export function proyectarDecision(respuesta: RespuestaSolicitud): ModeloDecision {
  switch (respuesta.accion) {
    case "REMITIR_PROCESO":
      return decisionRemitida(respuesta)
    case "SOLICITAR_INFORMACION":
      return decisionIncompleta(respuesta)
    case "DERIVAR_OPERADOR":
      return decisionDerivada(respuesta)
  }
}

function lectura(respuesta: RespuestaSolicitud) {
  return {
    resumen: respuesta.resumen,
    intencion: respuesta.intencion.tipo,
    confianza: respuesta.confianza,
    datosEncontrados: respuesta.datosEncontrados,
    datosFaltantes: respuesta.datosFaltantes,
    motivo: respuesta.motivo,
  }
}

function decisionRemitida(respuesta: RespuestaRemitir): DecisionRemitida {
  return {
    ...lectura(respuesta),
    estadoVisible: "Remitida",
    estado: "REMITIDA",
    accion: "REMITIR_PROCESO",
  }
}

function decisionIncompleta(respuesta: RespuestaSolicitarInformacion): DecisionIncompleta {
  return {
    ...lectura(respuesta),
    estadoVisible: "Incompleta",
    estado: "INCOMPLETA",
    accion: "SOLICITAR_INFORMACION",
    preguntas: respuesta.preguntas,
  }
}

function decisionDerivada(respuesta: RespuestaDerivar): DecisionDerivada {
  return {
    ...lectura(respuesta),
    estadoVisible: "Derivada",
    estado: "DERIVADA",
    accion: "DERIVAR_OPERADOR",
  }
}
