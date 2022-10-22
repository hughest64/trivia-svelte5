import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
    webServer: [
        {
            command: 'npm run build && npm run preview',
            port: 4173,
            // timeout: 10000
        }
        // TODO: possibly run a test django server as described at
        // https://docs.djangoproject.com/en/dev/ref/django-admin/#testserver
    ],
    use: { baseURL: 'http://localhost:4173' }
};

export default config;
