<script lang="ts">
    import { page } from '$app/stores';
    import { createSocket } from '$lib/utils';
    import { getContext, hasContext, setContext, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
    import handlers from '$stores/gameMessageHandlers';
    import type { SocketMessage } from '$stores/types';    

    const joincode = $page.params.joincode;
    const hasSocket = hasContext('socket');
    const socket: WebSocket =
        getContext('socket') ||
        (browser &&
            createSocket({
                socketUrl: `${apiHost}/ws${$page.url.pathname}/`,
                retryInterval: 1000,
                maxRetries: 50,
                retries: 0
            })
        );

    if (socket) {
        socket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);
            try {
                handlers[data.type](data.message);
            } catch {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };
    }
    
    !hasSocket && setContext('socket', socket);
    onDestroy(() => !!socket && socket.close());
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<slot />
