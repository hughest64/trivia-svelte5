<script lang="ts">
    import Socket from '$lib/Socket.svelte';
    import { page } from '$app/stores';
    import { socket } from '$stores/socket';
    import handlers from '$stores/gameMessageHandlers';
    import type { SocketMessage } from '$stores/types';

    $: if (!!$socket) {
        // console.log('adding message handler')
        $socket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);
            try {
                handlers[data.type](data.message);
            } catch {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };
    }
    const joincode = $page.params.joincode;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<Socket />

<slot />
