import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
    retries: 1,
    workers: 2,
    timeout: 30000,
    webServer: [
        {
            command: 'npm run build -- --mode test && npm run preview',
            port: 4173
        },
        {
            command: 'pipenv run python manage.py runserver 7000 --settings=server.settings_tst',
            cwd: 'server',
            port: 7000
        }
    ],
    use: { baseURL: 'http://127.0.0.1:4173' }
};

export default config;
