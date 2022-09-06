<script lang="ts">
    import { onDestroy, onMount } from 'svelte';
    import { page } from '$app/stores';
    import { socket } from '$stores/socket';
    import handlers from '$stores/gameMessageHandlers';
    import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
    import type { SocketMessage } from '$stores/types';

    const path = $page.url.pathname;

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
                handlers[data.type](data.message);
            } catch {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };

        return webSocket;
    };

    onMount(() => {
        if ($socket?.readyState !== 1) {
            $socket = createSocket();
        }
    });
    onDestroy(() => $socket?.close());
</script>
