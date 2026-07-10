import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Canonical domain: 25012004.xyz (custom domain on the Cloudflare Pages
// project "amarketer"; amarketer.pages.dev remains as alias).
export default defineConfig({
  site: 'https://25012004.xyz',
  integrations: [sitemap()],
  trailingSlash: 'never',
});
