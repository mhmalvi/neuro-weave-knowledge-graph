import { expect } from '@playwright/test';

module.exports = async () => {
  const base = process.env.MCP_BASE_URL;
  if (!base) throw new Error('MCP_BASE_URL missing in env');
};