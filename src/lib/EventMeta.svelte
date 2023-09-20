<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from './utils';

    const userData = getStore('userData');
    $: activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id);

    let copiedMsg = '';
    const handleCopyLink = () => {
        console.log('copying');
        navigator.clipboard.writeText('testing');
        copiedMsg = 'Copied to clipboard!';
    };
</script>

<div class="meta-container">
    <p class="title">Today's Join Codes</p>
    <div class="data">
        <span>Team Name</span>
        <strong>{activeTeam?.name || '-'}</strong>
    </div>
    <div class="data">
        <span>Team Password</span>
        <strong>{activeTeam?.password || '-'}</strong>
    </div>
    <div class="data">
        <span>Game Join Code</span>
        <strong>{$page.params.joincode || '-'}</strong>
    </div>
    {#if activeTeam}
        <button class="join-link" on:click={handleCopyLink}>
            Share <strong>this link</strong> to join team {copiedMsg}
        </button>
    {/if}
</div>

<style lang="scss">
    .meta-container {
        border: 2px solid var(--color-primary);
        padding: 0.5rem 1rem;
        display: flex;
        flex-direction: column;
    }
    .title {
        text-align: center;
        font-size: 1.5rem;
    }
    .data {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
    }
    span {
        font-weight: normal;
    }
    .join-link {
        margin: 1rem auto;
        color: var(--color-tertiary);
        font-weight: normal;
        font-size: 1rem;
    }
</style>
