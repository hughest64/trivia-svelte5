<script lange="ts">
    import { page } from '$app/stores';
    const logs = $page.data?.change_logs || [];
</script>

<svelte:head><title>Trivia Mafia | Changelog</title></svelte:head>

<main>
    <h1>Change Log</h1>

    <a href="/" class="button button-primary" data-sveltekit-reload>Return to the app</a>

    {#each logs as log (log.id)}
        <div>
            <h2 class="title">{log.title}</h2>
            <p class="version">{log.version} released {log.date}</p>
            <p class="notes">{log.notes}</p>
        </div>
    {/each}

    <a href="/" class="button button-primary" data-sveltekit-reload>Return to the app</a>
</main>

<style lang="scss">
    .title {
        font-weight: normal;
        font-size: 1.75rem;
    }
    .version {
        font-size: 1rem;
    }
    .notes {
        margin: 1rem 0 1.5rem;
    }
</style>
