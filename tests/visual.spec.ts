import { test, expect } from '@playwright/test';

test('homepage snapshot', async ({ page }) => {
  // Go to the homepage
  await page.goto('/');

  // Wait for the page to be fully loaded
  await page.waitForLoadState('networkidle');

  // Take a full page screenshot
  await page.screenshot({ path: 'screenshots/homepage.png', fullPage: true });
});
