import { defineConfig } from "vite";
const { resolve } = require('path');
import vue from '@vitejs/plugin-vue'
import Pages from "vite-plugin-pages";

// console.log(resolve("./"))

export default defineConfig({
  // plugins: [nodeResolve(), commonjs()],
  plugins: [vue(), Pages(
    {
      pagesDir: [
        {dir: "blog/src/pages", baseRoute: "blog/editor"}
      ]
    }

  )],
  root: "./website/templates",
  server: {
    fs: {
      // Allow serving files from one level up to the project root
      allow: ['..', resolve("./")]
    }
  },
  build: {
    chunkSizeWarningLimit: 1000,
    brotliSize: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve("./website/templates/main.js"),
        editor: resolve("./website/templates/blog/editor.js"),
    },
      },
    outDir: resolve("dist/"),
    },
  }
);
