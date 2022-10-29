<script lang="ts">
    import { getAllContexts, onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { page } from '$app/stores';
    import handlers from '$messages/player';
    import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
    import type { SocketMessage, StoreMap, StoreType } from '$lib/types';

    const path = $page.url.pathname;
    const stores = getAllContexts<StoreMap>();

    export let socketUrl = `${apiHost}/ws${path}/`;
    export let maxRetries = 50;
    export let retryInterval = 1000;
    export let reconnect = true;

    let interval: ReturnType<typeof setTimeout>;
    let retries = 0;

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);

        // TODO: we could just default to authenticating here by sending type: authenticate
        webSocket.onopen = () => {
            clearTimeout(interval);
            retries = 0;
        };
        webSocket.onclose = (event) => {
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                window.open('/user/logout', '_self');
            }
            if (!event.wasClean && event.code !== 4010 && reconnect && retries <= maxRetries) {
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                clearTimeout(interval);
            }
        };
        // TODO: dynamic handling (or importing?) for handler files based on game vs. host routes would be good
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);

            // no active_team_id
            if (data.type === 'unauthorized') {
                // TODO: set an errorMessage store?
                // I think we can do better than window.open, but goto is behaving strangly        
                window.open(`/team?next=${location.pathname}`, '_self');

            // aononymous user in the socket connection
            } else if (data.type === 'unauthenticated') {
                webSocket.send(JSON.stringify({ type: 'authenticate', message: { token: $page.data.jwt } }));

            } else if (handlers[data.type]) {
                handlers[data.type](data.message, <StoreType>stores.get(data.store));

            } else {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };

        return webSocket;
    };

    let socket: WebSocket;
    if (browser) socket = setContext<WebSocket>('socket', createSocket());
    onDestroy(() => socket?.close());
</script>

<slot />
