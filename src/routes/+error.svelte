<script lang="ts">
    import { page } from '$app/stores';
</script>

<main class="error-page">
    <h1>{$page.status}</h1>
    <h5>{$page.error?.message}</h5>
    {#if $page.error?.next && !$page.url.pathname.includes('host')}
        <p>click <a rel="external" href={$page.error.next}>here</a> to try again</p>
    {/if}
</main>
