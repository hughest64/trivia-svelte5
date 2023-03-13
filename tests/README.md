# Playwright Testing

### Tests for trivia events
- To avoid test files tripping over each other each `.spec` file should only use join codes not used by other files.
- Trivia Events with joincodes 9900 - 9910, all of which use the same game data, are available for testing and more can be added.
- [events.txt](/tests/events.txt) contains a list of events that are currently used in tests.
### Test Workers
- By default Playwright uses a separate worker instance per test file allowing test files to run in parallel.
- The [configuration file](/playwright.config.ts) currently limits workers to 2 to minimize flakiness.
### Testing in Production
- `NOTE:` this is a work in process and needs improvement
- To avoid conflicts the actual production build tests run against an identical but separate app build located at `.svelte-test` (the production build is located at `.svelte-kit`).
- In theory this prevents any disruption to currently connected clients during the test run but the app service does need to be restarted after each test run as clients get disconnected (for now).