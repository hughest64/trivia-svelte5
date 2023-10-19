<script lange="ts">
    import { page } from '$app/stores';
    const logs = $page.data?.change_logs || [];
</script>

<svelte:head><title>Trivia Mafia | Changelog</title></svelte:head>

<main>
    <h1>Change Log</h1>

    <a href="/" class="button button-primary" data-sveltekit-reload>Return to the app</a>

    <div>
        {#each logs as log (log.id)}
            <h2 class="title">{log.title}</h2>
            <p class="version">{log.version} released {log.date}</p>
            <div class="note-container">
                {#each log.notes.split('\n') as line}
                    <p class="notes">{line}</p>
                {/each}
            </div>
        {/each}
    </div>

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
    .note-container {
        margin: 1.5rem 0;
    }
    .notes {
        margin: 0;
    }
</style>
