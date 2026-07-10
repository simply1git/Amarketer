import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Canonical domain: amarketer.25012004.xyz (subdomain on the Cloudflare Pages
// project "amarketer"; root domain reserved for other projects;
// amarketer.pages.dev remains as alias).
export default defineConfig({
  site: 'https://amarketer.25012004.xyz',
  integrations: [sitemap()],
  trailingSlash: 'never',
});
