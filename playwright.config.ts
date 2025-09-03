import { defineConfig } from '@playwright/test';
import * as dotenv from 'dotenv';
dotenv.config();

const base = process.env.MCP_BASE_URL!;
const share = process.env.MCP_SHARE_TOKEN ? `?_vercel_share=${process.env.MCP_SHARE_TOKEN}` : '';

export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 60_000,
  use: {
    baseURL: base,
    extraHTTPHeaders: {
      // add anything MCP expects here later
    }
  },
  reporter: [['list'], ['html', { outputFolder: 'playwright-report' }]],
  globalSetup: require.resolve('./tests/e2e/_setup/global-asserts.ts'),
  metadata: { shareSuffix: share },
});