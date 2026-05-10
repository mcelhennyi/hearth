import { test, expect } from '@playwright/test'
import lighthouse from 'lighthouse'
import { mkdirSync, rmSync } from 'node:fs'
import { spawn, type ChildProcess } from 'node:child_process'
import net from 'node:net'
import path from 'node:path'
import { chromium } from 'playwright'

/** Lighthouse 12+ removed the `pwa` onlyCategories bucket; keep Lighthouse on 11.x until CI migrates to replacement audits. */
const previewOrigin = 'http://127.0.0.1:4173'

async function reservePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = net.createServer()
    server.unref()
    server.on('error', reject)
    server.listen(0, '127.0.0.1', () => {
      const address = server.address()
      if (typeof address === 'object' && address !== null) {
        const { port } = address
        server.close(() => resolve(port))
        return
      }
      server.close(() => reject(new Error('Unable to reserve a local port for Lighthouse')))
    })
  })
}

async function waitForChrome(remoteDebuggingPort: number): Promise<void> {
  const endpoint = `http://127.0.0.1:${remoteDebuggingPort}/json/version`
  const started = Date.now()
  let lastError: unknown

  while (Date.now() - started < 15_000) {
    try {
      const response = await fetch(endpoint)
      if (response.ok) {
        return
      }
    } catch (error) {
      lastError = error
    }
    await new Promise((resolve) => setTimeout(resolve, 250))
  }

  throw new Error(`Timed out waiting for Chromium CDP on ${endpoint}: ${String(lastError)}`)
}

function launchChromium(remoteDebuggingPort: number, userDataDir: string): ChildProcess {
  return spawn(
    chromium.executablePath(),
    [
      '--headless=new',
      `--remote-debugging-port=${remoteDebuggingPort}`,
      `--user-data-dir=${userDataDir}`,
      '--no-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
      'about:blank',
    ],
    { stdio: 'ignore' },
  )
}

test('Lighthouse PWA category score is at least 90', async () => {
  const remoteDebuggingPort = await reservePort()
  const userDataDir = path.join(process.cwd(), '.tmp', 'lighthouse-chrome')
  rmSync(userDataDir, { recursive: true, force: true })
  mkdirSync(userDataDir, { recursive: true })
  const chrome = launchChromium(remoteDebuggingPort, userDataDir)
  try {
    await waitForChrome(remoteDebuggingPort)
    const runnerResult = await lighthouse(`${previewOrigin}/`, {
      logLevel: 'error',
      output: 'json',
      onlyCategories: ['pwa'],
      port: remoteDebuggingPort,
    })
    const score = (runnerResult?.lhr?.categories?.pwa?.score ?? 0) * 100
    expect(score).toBeGreaterThanOrEqual(90)
  } finally {
    chrome.kill()
  }
})
