import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
    retries: 2,
    timeout: 60000, // 1 minute
    webServer: [
        {
            command: 'npm run build -- --mode test && npm run preview',
            port: 4173
        }
        // TODO: possibly run a test django server as described at
        // https://docs.djangoproject.com/en/dev/ref/django-admin/#testserver
    ],
    use: { baseURL: 'http://localhost:4173' }
};

export default config;
