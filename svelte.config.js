import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const testMode = process.env['MODE'] === 'test';
const envpath = process.env['ENV_PATH'] || '.';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://kit.svelte.dev/docs/integrations#preprocessors
    // for more information about preprocessors
    preprocess: vitePreprocess(),

    kit: {
        adapter: adapter({
            out: testMode ? 'build_test' : 'build'
        }),
        outDir: testMode ? '.svelte-test' : '.svelte-kit',
        env: { dir: envpath }
    },
    vitePlugin: { inspector: true }
};

export default config;
