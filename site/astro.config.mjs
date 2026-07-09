import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Update `site` when the custom domain lands; pages.dev subdomain until then.
export default defineConfig({
  site: 'https://solostack.pages.dev',
  integrations: [sitemap()],
  trailingSlash: 'never',
});
