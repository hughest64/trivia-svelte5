<script lang="ts">
	import { onMount, } from 'svelte'
    import { page } from '$app/stores'
    import { socket } from '$stores/socket'
	const apiHost = import.meta.env.VITE_API_HOST	
    const path = $page.url.pathname;
    const socketUrl = `${apiHost}/ws${path}/`

    onMount(() => {
        console.log(socketUrl);
        // const webSocket = new WebSocket(`${apiHost}/ws/${path}/`)
        // webSocket.onopen = () => console.log('connected')
        // webSocket.onclose = (event) => console.log('closing socket', event)

        // socket.set(webSocket)

        return () => console.log('unmounting')//webSocket.close(1001) // 1001 = endpoint is going away
    })
</script>