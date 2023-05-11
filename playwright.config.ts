import type { PlaywrightTestConfig } from '@playwright/test';

const testcmd = `
    npm run build:test &&\
    ORIGIN='http://127.0.0.1:4173'\
    HOST='127.0.0.1'\
    PORT=4173\
    node -r dotenv/config build_test dotenv_config_path=./.env.test
`;

const djangoservercmd = `
    DJANGO_SETTINGS_MODULE=server.settings_tst\
    pipenv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker\
    --bind 127.0.0.1:7000 server.asgi:application
`;

const config: PlaywrightTestConfig = {
    // retries: 1,
    workers: 3,
    timeout: 30000,
    webServer: [
        {
            command: testcmd,
            port: 4173
        },
        {
            command: djangoservercmd,
            cwd: 'server',
            port: 7000
        }
    ],
    use: { baseURL: 'http://127.0.0.1:4173' }
};

export default config;
