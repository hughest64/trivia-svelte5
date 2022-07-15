<script lang="ts">
	import { onMount, } from 'svelte'
    import { page } from '$app/stores'
    import { socket } from '$stores/socket'

	const apiHost = import.meta.env.VITE_WEBSOCKET_HOST	
    const path = $page.url.pathname;

    export let socketUrl = `${apiHost}/ws${path}/`
    export let maxRetries = 50
    export let retryInterval = 1000

    let interval: ReturnType<typeof setTimeout>
    let retries = 0
    
    const createSocket = () => {
        // console.log('conntection attempt', retries)
        const webSocket = new WebSocket(socketUrl)

        webSocket.onopen = () => {
            clearInterval(interval)
            retries = 0
            // console.log('connected')
        }
        webSocket.onclose = (event) => {  
            // console.log('closing socket', event)
            if (!event.wasClean && retries <= maxRetries) {
                retries ++
                setTimeout(createSocket, retryInterval)
            }
        }

        socket.set(webSocket);
        return webSocket
    }

    onMount(() => {
        // console.log('mounting')
        const webSocket = createSocket()
        return !!webSocket && webSocket.close
    })
</script>