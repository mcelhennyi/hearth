import { test, expect } from '@playwright/test'
import lighthouse from 'lighthouse'
import { launch as launchChrome } from 'chrome-launcher'
import { chromium } from 'playwright'

/** Lighthouse 12+ removed the `pwa` onlyCategories bucket; keep Lighthouse on 11.x until CI migrates to replacement audits. */
const previewOrigin = 'http://127.0.0.1:4173'

test('Lighthouse PWA category score is at least 90', async () => {
  const chrome = await launchChrome({
    chromePath: chromium.executablePath(),
    chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  })
  try {
    const runnerResult = await lighthouse(`${previewOrigin}/`, {
      logLevel: 'error',
      output: 'json',
      onlyCategories: ['pwa'],
      port: chrome.port,
    })
    const score = (runnerResult?.lhr?.categories?.pwa?.score ?? 0) * 100
    expect(score).toBeGreaterThanOrEqual(90)
  } finally {
    await chrome.kill()
  }
})
