import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import "@fontsource/manrope/400.css"
import "@fontsource/manrope/700.css"
import { PrevisualizacionDecision } from "./presentation/previsualizacion/PrevisualizacionDecision"

const raiz = document.getElementById("root")

if (!raiz) {
  throw new Error("No está el nodo raíz.")
}

createRoot(raiz).render(
  <StrictMode>
    <PrevisualizacionDecision />
  </StrictMode>,
)
