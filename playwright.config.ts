import type { PlaywrightTestConfig } from '@playwright/test';

/**
 * To test after code changes have been made to source use `npm run test:build` to test
 * which will build the project to the build_test directory with the proper variables.
 *
 * Subsequent test runs (if there are no code changes) can use `npm run test` which
 * eliminates the build step and saves time.
 */

const testcmd = `
    ORIGIN='http://127.0.0.1:4173'\
    HOST='127.0.0.1'\
    PORT=4173\
    node build_test
`;

const djangoservercmd = `
    pipenv run python manage.py migrate --settings=server.settings_tst &&\
    pipenv run python manage.py reset_test_data -a --settings=server.settings_tst &&\
    DJANGO_SETTINGS_MODULE=server.settings_tst\
    pipenv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker\
    --bind 127.0.0.1:7000 server.asgi:application
`;

const config: PlaywrightTestConfig = {
    // retries: 1,
    // workers: 3,
    timeout: 5000,
    webServer: [
        {
            command: testcmd,
            port: 4173
        },
        {
            command: djangoservercmd,
            cwd: 'server',
            port: 7000,
            // https://playwright.dev/docs/api/class-testconfig#test-config-web-server
            reuseExistingServer: true
        }
    ],
    use: { baseURL: 'http://127.0.0.1:4173' },
    testDir: 'tests_new'
};

export default config;
