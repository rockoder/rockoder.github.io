/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: '#0a0a0a',
          secondary: '#141414',
          tertiary: '#1a1a1a',
        },
        foreground: {
          DEFAULT: '#fafafa',
          muted: '#a1a1aa',
          subtle: '#71717a',
        },
        accent: {
          DEFAULT: '#10b981',
          hover: '#059669',
          muted: '#065f46',
        },
        border: {
          DEFAULT: '#27272a',
          hover: '#3f3f46',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Monaco', 'monospace'],
        serif: ['Georgia', 'Cambria', 'serif'],
      },
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': '#a1a1aa',
            '--tw-prose-headings': '#fafafa',
            '--tw-prose-lead': '#a1a1aa',
            '--tw-prose-links': '#10b981',
            '--tw-prose-bold': '#fafafa',
            '--tw-prose-counters': '#71717a',
            '--tw-prose-bullets': '#71717a',
            '--tw-prose-hr': '#27272a',
            '--tw-prose-quotes': '#a1a1aa',
            '--tw-prose-quote-borders': '#27272a',
            '--tw-prose-captions': '#71717a',
            '--tw-prose-code': '#fafafa',
            '--tw-prose-pre-code': '#fafafa',
            '--tw-prose-pre-bg': '#141414',
            '--tw-prose-th-borders': '#27272a',
            '--tw-prose-td-borders': '#27272a',
          },
        },
      },
    },
  },
  plugins: [],
};
