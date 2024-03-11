<script lang="ts">
    import { onDestroy, getContext, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { PUBLIC_WEBSOCKET_HOST } from '$env/static/public';
    import type { MessageHandler, RoundState, SocketMessage } from '$lib/types';
    import type { GameState } from './stores.svelte';

    let is_reconnect = false;
    let socketUrl = `${PUBLIC_WEBSOCKET_HOST}/ws/host/${$page.params.joincode}/`;
    let maxRetries = 50;
    let retryInterval = 1000;

    let interval: ReturnType<typeof setTimeout>;
    let retries = 0;

    let gameState = getContext<GameState>('gameState');

    // $inspect(gameState.locked_rounds);

    const handlers: MessageHandler = {
        connected: () => {
            // TODO in the case of reconnect, the may contain game data in the future
            console.log('connected!');
        },
        roundlock_s5: (msg: RoundState) => {
            gameState.updateRoundStates(msg);
        }
    };

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);
        webSocket.onopen = () => {
            clearTimeout(interval);
            retries = 0;
            is_reconnect && window.location.reload();
        };
        webSocket.onclose = (event) => {
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                goto('/user/logout', { invalidateAll: true });
            } else if (!event.wasClean && event.code !== 4010 && retries <= maxRetries) {
                // in the case of a device going to sleep, we lose the socket connection and have
                // the potential to be out of sync, in this case we want to reload the page after connecting
                is_reconnect = true;
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                clearTimeout(interval);
            }
        };
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);
            const msgType = data.msg_type;

            // no active_team_id
            if (msgType === 'unauthorized') {
                goto(`/team?next=${location.pathname}`, { invalidateAll: true });

                // anonymous user in the socket connection
            } else if (msgType === 'unauthenticated') {
                webSocket.send(JSON.stringify({ type: 'authenticate', message: { token: $page.data.jwt } }));
            } else if (handlers[msgType]) {
                handlers[msgType](data.message);
            } else {
                console.error(`message type ${msgType} does not have a handler function!`);
            }
        };

        return webSocket;
    };

    let socket: WebSocket;
    if (browser) socket = setContext<WebSocket>('socket', createSocket());
    onDestroy(() => socket?.close());
</script>

<slot />
