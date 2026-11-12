import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { describe, expect, it } from "vitest"

const src = join(dirname(fileURLToPath(import.meta.url)), "..")

function fuente(ruta: string): string {
  return readFileSync(join(src, ruta), "utf8")
}

describe("fronteras de la decisión", () => {
  it("el contrato no nombra las etiquetas de la pantalla", () => {
    const contrato = fuente("contract/respuesta-solicitud.ts")

    expect(contrato).not.toContain("Remitida")
    expect(contrato).not.toContain("Incompleta")
    expect(contrato).not.toContain("Derivada")
  })

  it("la vista no decide con el código de acción ni importa el contrato", () => {
    const vista = fuente("presentation/vista-decision/VistaDecision.tsx")

    expect(vista).not.toContain("REMITIR_PROCESO")
    expect(vista).not.toContain("SOLICITAR_INFORMACION")
    expect(vista).not.toContain("DERIVAR_OPERADOR")
    expect(vista).not.toContain("contract/")
  })

  it("el sistema de diseño no conoce las acciones del motor", () => {
    const diseno = fuente("presentation/design-system/andes-claro.css")

    expect(diseno).not.toContain("REMITIR_PROCESO")
    expect(diseno).not.toContain("SOLICITAR_INFORMACION")
    expect(diseno).not.toContain("DERIVAR_OPERADOR")
  })

  it("dominio, contrato y proyección no importan React ni CSS", () => {
    const capas = [
      "contract/respuesta-solicitud.ts",
      "domain/modelo-decision.ts",
      "application/proyectar-decision.ts",
    ]

    for (const capa of capas) {
      const texto = fuente(capa)
      expect(texto).not.toMatch(/from ["']react["']/)
      expect(texto).not.toMatch(/\.css["']/)
    }

    expect(fuente("domain/modelo-decision.ts")).not.toContain("contract/")
    expect(fuente("application/proyectar-decision.ts")).not.toContain("presentation/")
  })
})
