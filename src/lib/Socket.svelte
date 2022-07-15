<script lang="ts">
	import { onMount, } from 'svelte'
    import { page } from '$app/stores'
    import { socket } from '$stores/socket'

	const apiHost = import.meta.env.VITE_WEBSOCKET_HOST	
    const path = $page.url.pathname;
    export let socketUrl = `${apiHost}/ws${path}/`

    onMount(() => {
        console.log(socketUrl);
        const webSocket = new WebSocket(`${apiHost}/ws${path}`)
        webSocket.onopen = () => console.log('connected')
        webSocket.onclose = (event) => console.log('closing socket', event)

        socket.set(webSocket)

        return () => webSocket.close()
    })
</script>