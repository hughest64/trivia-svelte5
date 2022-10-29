<script lang="ts">
    import { getContext, onDestroy } from 'svelte';
    const socket = getContext<WebSocket>('socket');

    onDestroy(() => socket?.close());
</script>

<h1>Host - Chat</h1>
