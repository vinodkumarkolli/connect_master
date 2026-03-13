import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
import fs from 'fs'

// Safely load the config to prevent build breaks in Docker
const configPath = '../../../sites/common_site_config.json'
let commonConfig = {}
if (fs.existsSync(configPath)) {
  commonConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
}

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  // 1. Move logic INSIDE the function so it has access to 'command'
  const configPath = path.resolve(__dirname, '../../../sites/common_site_config.json')
  let webserverPort = 8000

  try {
    if (fs.existsSync(configPath)) {
      const commonConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
      webserverPort = commonConfig.webserver_port || 8000
    }
  } catch (e) {
    // In production/docker, we don't care if this fails
    console.warn('Using default port 8000 for proxy fallback.')
  }
  return {
    plugins: [vue()],
    server: command === 'serve' ? {
      port: 8080,
      proxy: getProxyOptions({
        port: webserverPort
      }),
    } : {},
    base: command === 'build' ? '/assets/connect_master/frontend/' : '/',
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    build: {
      outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
      emptyOutDir: true,
      target: 'es2015',
    },
    optimizeDeps: {
      include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
      esbuildOptions: {
        sourcemap: 'inline',
      },
    },
  }
})
