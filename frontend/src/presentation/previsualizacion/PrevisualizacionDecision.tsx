import { useState } from "react"
import { proyectarDecision } from "../../application/proyectar-decision"
import {
  fixtureDerivar,
  fixtureRemitir,
  fixtureSolicitarInformacion,
} from "../fixtures/decisiones"
import { VistaDecision } from "../vista-decision/VistaDecision"
import styles from "./PrevisualizacionDecision.module.css"

const OPCIONES = [
  { id: "remitir", etiqueta: "Remitida", respuesta: fixtureRemitir },
  { id: "incompleta", etiqueta: "Incompleta", respuesta: fixtureSolicitarInformacion },
  { id: "derivada", etiqueta: "Derivada", respuesta: fixtureDerivar },
] as const

type OpcionId = (typeof OPCIONES)[number]["id"]

export function PrevisualizacionDecision() {
  const [opcionId, setOpcionId] = useState<OpcionId>("remitir")
  const opcion = OPCIONES.find((candidata) => candidata.id === opcionId)

  if (!opcion) {
    return null
  }

  const decision = proyectarDecision(opcion.respuesta)

  return (
    <div className={`${styles.pagina} andes-pagina`}>
      <div className={styles.columna}>
        <p className={styles.marca}>Banco Andino</p>
        <p className={styles.contexto}>Tu caso, leído en una sola decisión.</p>
        <div className={styles.controles} role="group" aria-label="Estados de previsualización">
          {OPCIONES.map((candidata) => (
            <button
              key={candidata.id}
              type="button"
              className={styles.control}
              data-estado={candidata.etiqueta}
              aria-pressed={candidata.id === opcion.id}
              onClick={() => setOpcionId(candidata.id)}
            >
              {candidata.etiqueta}
            </button>
          ))}
        </div>
        <VistaDecision decision={decision} />
      </div>
    </div>
  )
}
