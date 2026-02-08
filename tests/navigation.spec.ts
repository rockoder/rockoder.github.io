import { test, expect } from '@playwright/test';

test('navigation from home should show Back to Home', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Find a blog post link in the home page (usually in the latest posts section)
  const blogPostLink = page.locator('a[href^="/blog/"]:not([href="/blog/"])').first();
  await blogPostLink.click();
  await page.waitForLoadState('networkidle');

  const backLink = page.locator('#back-link');
  await expect(backLink).toBeVisible();
  await expect(backLink).toContainText('Back to Home');
  await expect(backLink).toHaveAttribute('href', '/');
});

test('navigation from blog index should show Back to all posts', async ({ page }) => {
  await page.goto('/blog/');
  await page.waitForLoadState('networkidle');

  // Find a blog post link in the blog index
  const blogPostLink = page.locator('a[href^="/blog/"]:not([href="/blog/"])').first();
  await blogPostLink.click();
  await page.waitForLoadState('networkidle');

  const backLink = page.locator('#back-link');
  await expect(backLink).toBeVisible();
  await expect(backLink).toContainText('Back to all posts');
  await expect(backLink).toHaveAttribute('href', '/blog/');
});

test('direct navigation to blog post should show Back to all posts', async ({ page }) => {
  // Direct navigation has no referrer within the same origin
  await page.goto('/blog/humans-md/');
  await page.waitForLoadState('networkidle');

  const backLink = page.locator('#back-link');
  await expect(backLink).toBeVisible();
  await expect(backLink).toContainText('Back to all posts');
  await expect(backLink).toHaveAttribute('href', '/blog/');
});
