import { test, expect, request } from '@playwright/test';

const share = process.env.MCP_SHARE_TOKEN ? `?_vercel_share=${process.env.MCP_SHARE_TOKEN}` : '';

test.describe('MCP Server @smoke', () => {
  test('Root HTML responds 200', async ({ page }) => {
    await page.goto('/' + (share ? share : ''), { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveTitle(/.+/); // any title means HTML served
  });

  test('GET /api/mcp returns 501 (unsupported method)', async ({ request }) => {
    const res = await request.get(`/api/mcp${share}`);
    expect(res.status()).toBe(501); // Your log showed 501 = correct "alive but method wrong"
  });

  test('POST /api/mcp handles minimal payload (no 5xx)', async ({ request }) => {
    // Adjust body to the simplest MCP ping your server tolerates
    const body = { ping: true };
    const res = await request.post(`/api/mcp${share}`, {
      data: body,
      headers: { 'content-type': 'application/json' },
    });
    expect([200, 400, 401, 403, 405]).toContain(res.status());
    // Absolutely no 5xx allowed
  });
});