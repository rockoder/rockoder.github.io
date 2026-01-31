#!/usr/bin/env node

/**
 * Migration script to convert Jekyll posts to Astro content collections
 *
 * Usage: node scripts/migrate-posts.mjs
 */

import { readdir, readFile, writeFile, mkdir, cp } from 'fs/promises';
import { join, basename } from 'path';
import { existsSync } from 'fs';

const POSTS_DIR = './_posts';
const BLOG_DIR = './src/content/blog';
const NOTES_DIR = './src/content/notes';
const PUBLIC_DIR = './public';

// Create output directories
async function ensureDirs() {
  for (const dir of [BLOG_DIR, NOTES_DIR, `${PUBLIC_DIR}/images/posts`, `${PUBLIC_DIR}/images/tweets`]) {
    if (!existsSync(dir)) {
      await mkdir(dir, { recursive: true });
    }
  }
}

// Parse frontmatter from markdown file
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: content };
  }

  const frontmatterStr = match[1];
  const body = match[2];

  // Simple YAML parsing
  const frontmatter = {};
  const lines = frontmatterStr.split('\n');

  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value = line.slice(colonIndex + 1).trim();

    // Handle quoted strings
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    frontmatter[key] = value;
  }

  return { frontmatter, body };
}

// Extract slug from Jekyll filename (YYYY-MM-DD-slug.md -> slug)
function extractSlug(filename) {
  const match = filename.match(/^\d{4}-\d{2}-\d{2}-(.+)\.md$/);
  return match ? match[1] : filename.replace('.md', '');
}

// Extract date from Jekyll filename
function extractDate(filename) {
  const match = filename.match(/^(\d{4}-\d{2}-\d{2})/);
  return match ? match[1] : null;
}

// Convert Jekyll post to Astro format
function convertBlogPost(filename, content) {
  const { frontmatter, body } = parseFrontmatter(content);
  const slug = extractSlug(filename);
  const dateFromFilename = extractDate(filename);

  // Build new frontmatter
  const newFrontmatter = {
    title: frontmatter.title || slug.replace(/-/g, ' '),
    date: frontmatter.date || dateFromFilename,
    author: frontmatter.author === 'rockoder' ? 'Ganesh Pagade' : (frontmatter.author || 'Ganesh Pagade'),
    tags: [],
    draft: false,
  };

  // Parse tags (handle Jekyll's YAML array format)
  if (frontmatter.tags) {
    const tagsStr = frontmatter.tags;
    // Handle comma-separated list with dash prefix
    if (tagsStr.startsWith('-')) {
      newFrontmatter.tags = [tagsStr.slice(1).trim()];
    } else {
      // Parse comma-separated tags
      newFrontmatter.tags = tagsStr.split(',').map(t => t.trim()).filter(Boolean);
    }
  }

  // Convert body - fix image paths
  let newBody = body
    .replace(/\{\{\s*site\.baseurl\s*\}\}/g, '')
    .replace(/\/assets\/images\//g, '/images/')
    .replace(/\{\%.*?\%\}/g, ''); // Remove liquid tags

  // Build new content
  const newContent = `---
title: "${newFrontmatter.title.replace(/"/g, '\\"')}"
date: ${newFrontmatter.date}
author: "${newFrontmatter.author}"
tags: [${newFrontmatter.tags.map(t => `"${t}"`).join(', ')}]
draft: ${newFrontmatter.draft}
---

${newBody.trim()}
`;

  return { slug, content: newContent };
}

// Convert Jekyll tweet post to Astro notes format
function convertNotePost(filename, content) {
  const { frontmatter, body } = parseFrontmatter(content);
  const slug = extractSlug(filename);
  const dateFromFilename = extractDate(filename);

  // Build new frontmatter
  const newFrontmatter = {
    title: frontmatter.title || '',
    date: frontmatter.date || dateFromFilename,
    tweet_url: frontmatter.tweet_url || '',
    tweet_id: frontmatter.tweet_id || '',
    screenshot: frontmatter.screenshot ? frontmatter.screenshot.replace('/assets/images/', '/images/') : '',
  };

  // Build new content
  const newContent = `---
title: "${newFrontmatter.title.replace(/"/g, '\\"')}"
date: ${newFrontmatter.date}
tweet_url: "${newFrontmatter.tweet_url}"
tweet_id: "${newFrontmatter.tweet_id}"
screenshot: "${newFrontmatter.screenshot}"
---

${body.trim()}
`;

  return { slug, content: newContent };
}

// Generate redirect map for legacy URLs
function generateRedirectMap(posts) {
  const redirects = {};

  for (const post of posts) {
    const filename = post.filename;
    const slug = post.slug;
    const type = post.type;

    // Extract date parts from filename
    const dateMatch = filename.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (dateMatch) {
      const [, year, month, day] = dateMatch;
      const oldPath = `/${year}/${month}/${day}/${slug}/`;
      const newPath = type === 'blog' ? `/blog/${slug}/` : `/notes/${slug}/`;
      redirects[oldPath] = newPath;
    }
  }

  return redirects;
}

async function main() {
  console.log('Starting migration...\n');

  await ensureDirs();

  // Read all posts
  const files = await readdir(POSTS_DIR);
  const mdFiles = files.filter(f => f.endsWith('.md'));

  console.log(`Found ${mdFiles.length} posts to migrate\n`);

  const blogPosts = [];
  const notePosts = [];
  const processedPosts = [];

  for (const filename of mdFiles) {
    const filepath = join(POSTS_DIR, filename);
    const content = await readFile(filepath, 'utf-8');
    const { frontmatter } = parseFrontmatter(content);

    const isTweet = frontmatter.layout === 'tweet' || filename.includes('tweet-');

    if (isTweet) {
      const { slug, content: newContent } = convertNotePost(filename, content);
      notePosts.push({ filename, slug, content: newContent });
      processedPosts.push({ filename, slug, type: 'notes' });

      // Write to notes directory
      await writeFile(join(NOTES_DIR, `${slug}.md`), newContent);
      console.log(`  [note] ${slug}`);
    } else {
      const { slug, content: newContent } = convertBlogPost(filename, content);
      blogPosts.push({ filename, slug, content: newContent });
      processedPosts.push({ filename, slug, type: 'blog' });

      // Write to blog directory
      await writeFile(join(BLOG_DIR, `${slug}.md`), newContent);
      console.log(`  [blog] ${slug}`);
    }
  }

  console.log(`\nMigrated:`);
  console.log(`  - ${blogPosts.length} blog posts`);
  console.log(`  - ${notePosts.length} notes/tweets`);

  // Generate redirect map
  const redirects = generateRedirectMap(processedPosts);
  const redirectsContent = `// Auto-generated redirect map for legacy URLs
// Add these to astro.config.mjs redirects section

export const legacyRedirects = ${JSON.stringify(redirects, null, 2)};
`;

  await writeFile('./src/data/redirects.ts', redirectsContent);
  console.log(`\nGenerated redirect map with ${Object.keys(redirects).length} entries`);

  // Copy assets
  console.log('\nCopying assets...');

  // Copy images
  if (existsSync('./assets/images')) {
    await cp('./assets/images', `${PUBLIC_DIR}/images`, { recursive: true });
    console.log('  Copied images');
  }

  // Copy favicon and other root assets
  if (existsSync('./assets/images/favicon.ico')) {
    await cp('./assets/images/favicon.ico', `${PUBLIC_DIR}/favicon.ico`);
    console.log('  Copied favicon.ico');
  }

  // Copy Resume.pdf
  if (existsSync('./assets/Resume.pdf')) {
    await cp('./assets/Resume.pdf', `${PUBLIC_DIR}/Resume.pdf`);
    console.log('  Copied Resume.pdf');
  }

  // Copy CNAME
  if (existsSync('./CNAME')) {
    await cp('./CNAME', `${PUBLIC_DIR}/CNAME`);
    console.log('  Copied CNAME');
  }

  console.log('\nMigration complete!');
}

main().catch(console.error);
