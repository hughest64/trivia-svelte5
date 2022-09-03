<script lang="ts">
    import { page } from '$app/stores';
    import  { createSocket } from '$lib/utils';
    import { setContext, onDestroy } from 'svelte';
    // import type { PageData } from './$types';

    // export let data: PageData;
  

    /**
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
    */
    const joincode = $page.params.joincode;

    const socket = createSocket({
        socketUrl: 'url',
        retryInterval: 1000,
        maxRetries: 50,
        retries: 0
    });
    setContext('socket', socket);

    onDestroy(() => !!socket && socket.close());

</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<!-- <Socket /> -->

<slot />
