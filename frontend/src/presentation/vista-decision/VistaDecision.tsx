import { useEffect, useRef, useState, type ReactNode } from "react"
import type { EstadoVisible, ModeloDecision } from "../../domain/modelo-decision"
import "../design-system/andes-claro.css"
import styles from "./VistaDecision.module.css"

type Props = {
  decision: ModeloDecision
}

const MENSAJE_ACCION: Record<EstadoVisible, string> = {
  Remitida: "La solicitud pasó al proceso que la resuelve.",
  Incompleta: "La intención se sostiene y faltan datos.",
  Derivada: "Un operador continúa la atención.",
}

export function VistaDecision({ decision }: Props) {
  return (
    <article key={decision.estadoVisible} className={`${styles.tarjeta} andes-vidrio`} data-estado={decision.estadoVisible}>
      <Entrada orden={0}>
        <p className={`${styles.pastilla} andes-pastilla`} data-estado={decision.estadoVisible}>
          {decision.estadoVisible}
        </p>
      </Entrada>
      <Entrada orden={1}>
        <div className={styles.lineaOro} />
      </Entrada>
      <Entrada orden={2}>
        <h1 className={styles.resumen}>{decision.resumen}</h1>
      </Entrada>
      <Entrada orden={3}>
        <Campo titulo="Intención" texto={decision.intencion} />
      </Entrada>
      <Entrada orden={4}>
        <section className={styles.seccion}>
          <h2>Confianza</h2>
          <p className={styles.confianzaValor}>{textoConfianza(decision.confianza)}</p>
        </section>
      </Entrada>
      <Entrada orden={5}>
        <div className={styles.columnas}>
          <ListaDatos titulo="Datos encontrados" datos={decision.datosEncontrados} />
          <DatosFaltantes datos={decision.datosFaltantes} />
        </div>
      </Entrada>
      <Entrada orden={6}>
        <section className={`${styles.seccion} ${styles.accion}`}>
          <h2>Acción</h2>
          <p>{MENSAJE_ACCION[decision.estadoVisible]}</p>
          <p className={styles.codigo}>{decision.accion}</p>
        </section>
      </Entrada>
      <Entrada orden={7}>
        <Campo titulo="Motivo" texto={decision.motivo} />
      </Entrada>
      {decision.estadoVisible === "Incompleta" ? (
        <Entrada orden={8}>
          <Preguntas preguntas={decision.preguntas} />
        </Entrada>
      ) : null}
    </article>
  )
}

function Entrada({ children, orden }: { children: ReactNode; orden: number }) {
  const ref = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const nodo = ref.current
    if (!nodo || prefiereSinMovimiento() || !("IntersectionObserver" in window)) {
      setVisible(true)
      return
    }

    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (!entrada?.isIntersecting) {
          return
        }
        setVisible(true)
        observador.disconnect()
      },
      { rootMargin: "0px 0px 12% 0px", threshold: 0.05 },
    )
    observador.observe(nodo)
    return () => observador.disconnect()
  }, [])

  const demora = orden <= 4 ? orden * 55 : 0

  return (
    <div
      ref={ref}
      className={`${styles.entrada} ${demora === 0 ? styles.entradaPronta : ""} ${visible ? styles.entradaVisible : ""}`}
      style={{ transitionDelay: `${demora}ms` }}
    >
      {children}
    </div>
  )
}

function prefiereSinMovimiento(): boolean {
  if (typeof window.matchMedia !== "function") {
    return false
  }
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
}

function textoConfianza(confianza: number): string {
  return new Intl.NumberFormat("es-CO", {
    style: "percent",
    maximumFractionDigits: 0,
  })
    .format(confianza)
    .replaceAll("\u00a0", " ")
    .replaceAll("\u202f", " ")
}

function Campo({ titulo, texto }: { titulo: string; texto: string }) {
  return (
    <section className={styles.seccion}>
      <h2>{titulo}</h2>
      <p>{texto}</p>
    </section>
  )
}

function ListaDatos({ titulo, datos }: { titulo: string; datos: readonly string[] }) {
  return (
    <section className={`${styles.seccion} ${styles.panel}`}>
      <h2>{titulo}</h2>
      <ul className={styles.datos}>
        {datos.map((dato) => (
          <li key={dato}>{dato}</li>
        ))}
      </ul>
    </section>
  )
}

function DatosFaltantes({ datos }: { datos: readonly string[] }) {
  return (
    <section className={`${styles.seccion} ${styles.panel}`}>
      <h2>Datos faltantes</h2>
      {datos.length === 0 ? (
        <p>No falta nada.</p>
      ) : (
        <ul className={styles.datos}>
          {datos.map((dato) => (
            <li key={dato}>{dato}</li>
          ))}
        </ul>
      )}
    </section>
  )
}

function Preguntas({ preguntas }: { preguntas: readonly string[] }) {
  return (
    <section className={styles.seccion}>
      <h2>Preguntas</h2>
      <ol className={styles.preguntas} aria-label="Preguntas">
        {preguntas.map((pregunta) => (
          <li key={pregunta}>{pregunta}</li>
        ))}
      </ol>
    </section>
  )
}
