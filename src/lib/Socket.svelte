<script lang="ts">
    import { onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
    import MessageHandlers from '$lib/MessageHandlers.svelte';

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
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                goto('/user/logout', { invalidateAll: true });
            } else if (!event.wasClean && event.code !== 4010 && reconnect && retries <= maxRetries) {
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                clearTimeout(interval);
            }
        };
        return webSocket;
    };

    let socket: WebSocket;
    if (browser) socket = setContext<WebSocket>('socket', createSocket());
    onDestroy(() => socket?.close());
</script>

<MessageHandlers />
<slot />
