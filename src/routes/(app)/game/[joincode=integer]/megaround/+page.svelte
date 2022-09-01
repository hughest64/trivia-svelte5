<script lang="ts">
    import { onDestroy } from 'svelte';
    import { page } from '$app/stores';
    const { socket } = $page.data;

    // TODO: this works but would have to be repeated in each page
    // and leads to lots of connects and disconnect that shouldn't be necessary
    onDestroy(() => {
        socket && socket.close();
    });
</script>

<h1>Game - Megaround</h1>
