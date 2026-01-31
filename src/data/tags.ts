import { getCollection } from 'astro:content';

export interface TagData {
  tag: string;
  count: number;
  fontSize: number; // Normalized font size (0.75 to 1.5 rem)
}

// Cache for tag data (computed once at build time)
let cachedTagData: TagData[] | null = null;

/**
 * Aggregates tag counts across all published posts.
 * Uses build-time caching to avoid N+1 queries.
 */
export async function getTagCloud(): Promise<TagData[]> {
  if (cachedTagData) {
    return cachedTagData;
  }

  const posts = await getCollection('blog', ({ data }) => !data.draft);

  // Aggregate tag counts
  const tagCounts = new Map<string, number>();

  for (const post of posts) {
    const tags = post.data.tags || [];
    for (const tag of tags) {
      const normalizedTag = tag.toLowerCase().trim();
      tagCounts.set(normalizedTag, (tagCounts.get(normalizedTag) || 0) + 1);
    }
  }

  // Convert to array and sort alphabetically
  const tags = Array.from(tagCounts.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => a.tag.localeCompare(b.tag));

  // Normalize counts to font sizes
  cachedTagData = normalizeFontSizes(tags);

  return cachedTagData;
}

/**
 * Normalizes tag counts to a bounded font size range.
 * Uses linear scaling with log fallback for highly skewed distributions.
 */
function normalizeFontSizes(tags: { tag: string; count: number }[]): TagData[] {
  if (tags.length === 0) return [];

  const counts = tags.map((t) => t.count);
  const minCount = Math.min(...counts);
  const maxCount = Math.max(...counts);

  // Font size range (in rem)
  const minFontSize = 0.8;
  const maxFontSize = 1.4;

  // Check if distribution is highly skewed (max > 5x min)
  const isSkewed = maxCount > minCount * 5;

  return tags.map(({ tag, count }) => {
    let normalizedValue: number;

    if (maxCount === minCount) {
      // All tags have same count
      normalizedValue = 0.5;
    } else if (isSkewed) {
      // Use logarithmic scaling for skewed distributions
      const logMin = Math.log(minCount);
      const logMax = Math.log(maxCount);
      const logCount = Math.log(count);
      normalizedValue = (logCount - logMin) / (logMax - logMin);
    } else {
      // Use linear scaling
      normalizedValue = (count - minCount) / (maxCount - minCount);
    }

    const fontSize = minFontSize + normalizedValue * (maxFontSize - minFontSize);

    return {
      tag,
      count,
      fontSize: Math.round(fontSize * 100) / 100, // Round to 2 decimal places
    };
  });
}

/**
 * Get all unique tags sorted alphabetically
 */
export async function getAllTags(): Promise<string[]> {
  const tagCloud = await getTagCloud();
  return tagCloud.map((t) => t.tag);
}

/**
 * Get posts by tag
 */
export async function getPostsByTag(tag: string) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.filter((post) =>
    (post.data.tags || []).some((t) => t.toLowerCase() === tag.toLowerCase())
  );
}
