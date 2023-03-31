import type { PlaywrightTestConfig } from '@playwright/test';

const testcmd = `
    npm run build:test &&\
    ORIGIN='http://127.0.0.1:4173'\
    HOST='127.0.0.1'\
    PORT=4173\
    node -r dotenv/config build_test dotenv_config_path=./.env.test
`;

const config: PlaywrightTestConfig = {
    // retries: 1,
    workers: 2,
    timeout: 30000,
    webServer: [
        {
            // command: 'npm run build:test && npm run preview:test -- --mode test',
            command: testcmd,
            port: 4173
        },
        {
            command: 'DJANGO_SETTINGS_MODULE=server.settings_tst pipenv run daphne -p 7000 server.asgi:application ',
            cwd: 'server',
            port: 7000
        }
    ],
    use: { baseURL: 'http://127.0.0.1:4173' }
};

export default config;
