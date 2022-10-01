<script lang="ts">
    import { onDestroy, getAllContexts, getContext, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { page } from '$app/stores';
    import handlers from '$messages/player';
    import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
    import type { SocketMessage, StoreKey, StoreMap, StoreType } from '$lib/types';

    const path = $page.url.pathname;
    const stores: StoreMap = getAllContexts();

    export let socketUrl = `${apiHost}/ws${path}/`;
    export let maxRetries = 50;
    export let retryInterval = 1000;
    export let reconnect = true;

    let interval: ReturnType<typeof setTimeout>;
    let retries = 0;    

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);

        webSocket.onopen = () => {
            clearTimeout(interval);
            retries = 0;
        };
        webSocket.onclose = (event) => {
            if (!event.wasClean && reconnect && retries <= maxRetries) {
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                clearTimeout(interval);
            }
        };
        // TODO: dynamic handling (or importing?) for handler files based on game vs. host routes would be good
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);

            try {
                handlers[data.type](data.message, <StoreType>stores.get(<StoreKey>data.store));
            } catch {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };

        return webSocket;
    };

    const socket: WebSocket = getContext('socket');
    socket?.readyState !== 1 && browser && setContext('socket', createSocket());

    onDestroy(() => socket?.close());
</script>

<slot />
