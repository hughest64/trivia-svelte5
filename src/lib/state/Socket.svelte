<script lang="ts">
    import { getContext } from 'svelte';
    import { getState } from './utils.svelte';
    import type { MessageHandler, SocketMessage } from '$lib/types';

    const evh = getState('eventHandler');

    const webSocket = getContext<WebSocket>('socket');

    const handlers: MessageHandler = {
        connected: () => {
            console.log('connected via svelte 5!');
        },
        round_update: (msg: any) => {
            console.log(msg);
            // add a method to the event handler and call it with msg!
            // it should be that easy
        }
    };

    $effect(() => {
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);
            const msgType = data.msg_type;
            if (handlers[msgType]) {
                handlers[msgType](data.message);
            }
        };
    });
</script>
