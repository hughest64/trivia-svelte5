<script lang="ts">
    import { onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    // TODO: add the socket host to page data via the handle hook to avoid the variable import here
    import { env } from '$env/dynamic/public';
    import MessageHandlers from '$lib/MessageHandlers.svelte';

    const path = $page.url.pathname;
    const socketHost = env.PUBLIC_WEBSOCKET_HOST;
    export let socketUrl = `${socketHost}/ws${path}/`;
    export let maxRetries = 50;
    export let retryInterval = 1000;
    export let reconnect = true;

    let interval: ReturnType<typeof setTimeout>;
    let retries = 0;

    // TODO: something is causing an issue with reconnection of the socket when the server goes down and comes back online
    // reloading the page 'fixes' the issue, but we should seek a proper solution as this is very inefficient
    let loaded = false;
    let needsreload = false;
    $: if (loaded && needsreload) {
        window.location.reload();
    }

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);
        webSocket.onopen = () => {
            loaded = true;
            clearTimeout(interval);
            retries = 0;
        };
        webSocket.onclose = (event) => {
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                goto('/user/logout', { invalidateAll: true });
            } else if (!event.wasClean && event.code !== 4010 && reconnect && retries <= maxRetries) {
                needsreload = true;
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                needsreload = false;
                clearTimeout(interval);
            }
            loaded = false;
        };
        return webSocket;
    };

    let socket: WebSocket;
    if (browser) socket = setContext<WebSocket>('socket', createSocket());
    onDestroy(() => {
        socket?.close();
    });
</script>

<MessageHandlers />
<slot />
