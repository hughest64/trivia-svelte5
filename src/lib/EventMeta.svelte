<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from './utils';

    $: url = $page.url;
    const userData = getStore('userData');
    $: activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id);

    let copiedMsg = '';
    const handleCopyLink = () => {
        const link = `${url.origin}/team/join?password=${activeTeam?.password || ''}`;
        navigator.clipboard.writeText(link);
        copiedMsg = 'Copied to clipboard!';
    };
</script>

<div class="meta-container">
    <div class="data">
        <strong>Game Join Code:</strong>
        <strong>{$page.params.joincode || '-'}</strong>
    </div>
    <!-- {#if activeTeam}
        <button class="join-link" on:click={handleCopyLink}>
            Share <strong>this link</strong> to join team {copiedMsg}
        </button>
    {/if} -->
</div>

<style lang="scss">
    .meta-container {
        border: 2px solid var(--color-primary);
        padding: 0.5rem 1rem;
        display: flex;
        flex-direction: column;
    }
    .data {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
    }

    // .join-link {
    //     margin: 1rem auto;
    //     color: var(--color-tertiary);
    //     font-weight: normal;
    //     font-size: 1rem;
    // }
</style>
