import react from "@vitejs/plugin-react"
import { defineConfig } from "vitest/config"

const enGitHubPages = process.env.GITHUB_PAGES === "true"

export default defineConfig({
  base: enGitHubPages ? "/banco_andino_nlu_engine/" : "/",
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
  },
})
