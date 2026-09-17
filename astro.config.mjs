import { defineConfig } from 'astro/config';
const [owner, repo] = (process.env.GITHUB_REPOSITORY || '').split('/');
const site = process.env.SITE_URL || (owner ? `https://${owner.toLowerCase()}.github.io` : 'https://example.org');
const base = process.env.SITE_BASE ?? (owner && repo.toLowerCase() !== `${owner.toLowerCase()}.github.io` ? `/${repo}` : '/');
export default defineConfig({
  site, base, output: 'static', trailingSlash: 'always',
  i18n: { locales: ['en', 'ko'], defaultLocale: 'en', routing: { prefixDefaultLocale: false } },
  build: { format: 'directory' },
});
