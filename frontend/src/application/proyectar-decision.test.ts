import { describe, expect, it } from "vitest"
import {
  fixtureDerivar,
  fixtureRemitir,
  fixtureSinDatosFaltantes,
  fixtureSolicitarInformacion,
} from "../presentation/fixtures/decisiones"
import { proyectarDecision } from "./proyectar-decision"

describe("proyección de la decisión", () => {
  it("remitir se ve como Remitida y no lleva preguntas", () => {
    const decision = proyectarDecision(fixtureRemitir)

    expect(decision.estadoVisible).toBe("Remitida")
    expect(decision.estado).toBe("REMITIDA")
    expect(decision.accion).toBe("REMITIR_PROCESO")
    expect(decision.intencion).toBe("devolución pendiente")
    expect("preguntas" in decision).toBe(false)
  })

  it("pedir información se ve como Incompleta y conserva las preguntas", () => {
    const decision = proyectarDecision(fixtureSolicitarInformacion)

    expect(decision.estadoVisible).toBe("Incompleta")
    expect(decision.estado).toBe("INCOMPLETA")
    if (decision.estadoVisible !== "Incompleta") {
      return
    }
    expect(decision.preguntas).toEqual(fixtureSolicitarInformacion.preguntas)
  })

  it("derivar se ve como Derivada y no lleva preguntas", () => {
    const decision = proyectarDecision(fixtureDerivar)

    expect(decision.estadoVisible).toBe("Derivada")
    expect(decision.estado).toBe("DERIVADA")
    expect(decision.accion).toBe("DERIVAR_OPERADOR")
    expect("preguntas" in decision).toBe(false)
  })

  it("sin datos faltantes la colección de la vista queda vacía", () => {
    const decision = proyectarDecision(fixtureSinDatosFaltantes)

    expect(decision.datosFaltantes).toEqual([])
  })
})
