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
        const webSocket = new WebSocket(socketUrl)

        webSocket.onopen = () => {
            clearInterval(interval)
            retries = 0
            // console.log('connected')
        }
        // webSocket.onerror = (e) => {
        //     console.log(e)
        // }
        webSocket.onclose = (event) => {  
            // console.log('closing socket')
            if (!event.wasClean && retries <= maxRetries) {
                retries ++
                setTimeout(createSocket, retryInterval)
            } else {
                // TODO: We could set a message letting the user know the connection died
                clearTimeout(interval);
            }
        }

        socket.set(webSocket);
    }

    onMount(() => {
        createSocket()
        return !!$socket && $socket.close
    })
</script>