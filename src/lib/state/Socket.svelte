<script lang="ts">
    import { getContext } from 'svelte';
    import { getState } from './utils.svelte';
    import type { MessageHandler, RoundState, SocketMessage } from '$lib/types';

    const evh = getState('eventHandler');

    const webSocket = getContext<WebSocket>('socket');

    const handlers: MessageHandler = {
        connected: () => {
            console.log('connected via svelte 5!');
        },
        // TODO: s5 responses and response_summary are also in this payload
        round_update: (msg: Record<string, RoundState>) => {
            evh.updateRoundState(msg.round_state);
            // responses are updated only if the statis locked
            // unsure why only if locked, or if we event care about resps being locked?
            // responseSummaryStore also gets set
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
