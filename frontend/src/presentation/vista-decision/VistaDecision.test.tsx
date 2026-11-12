import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { proyectarDecision } from "../../application/proyectar-decision"
import {
  fixtureDerivar,
  fixtureRemitir,
  fixtureSinDatosFaltantes,
  fixtureSolicitarInformacion,
} from "../fixtures/decisiones"
import { VistaDecision } from "./VistaDecision"

const ETIQUETAS = ["Remitida", "Incompleta", "Derivada"] as const

describe("vista de la decisión", () => {
  it("cada fixture muestra una sola etiqueta y las preguntas solo en Incompleta", () => {
    const fixtures = [fixtureRemitir, fixtureSolicitarInformacion, fixtureDerivar, fixtureSinDatosFaltantes]

    for (const fixture of fixtures) {
      const decision = proyectarDecision(fixture)
      const vista = render(<VistaDecision decision={decision} />)

      expect(screen.getAllByText(decision.estadoVisible)).toHaveLength(1)
      for (const etiqueta of ETIQUETAS) {
        if (etiqueta !== decision.estadoVisible) {
          expect(screen.queryByText(etiqueta)).not.toBeInTheDocument()
        }
      }

      if (decision.estadoVisible === "Incompleta") {
        expect(screen.getByRole("list", { name: "Preguntas" })).toBeInTheDocument()
        for (const pregunta of decision.preguntas) {
          expect(screen.getByText(pregunta)).toBeInTheDocument()
        }
      } else {
        expect(screen.queryByRole("list", { name: "Preguntas" })).not.toBeInTheDocument()
      }

      if (decision.datosFaltantes.length === 0) {
        expect(screen.getByText("No falta nada.")).toBeInTheDocument()
      }

      expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
      vista.unmount()
    }
  })
})
