<script lang="ts">
    import { page } from '$app/stores';
    import { deserialize } from '$app/forms';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;

    const adjustmentReasons = $page.data.points_adjustment_reasons || [];
    // $: console.log($page.data);

    let adjustmentPoints = entry.points_adjustment_value;
    let adjustmentReason = entry.points_adjustment_reason_id;

    let error: string;

    const handleSetAdjustmentPoints = async (direction: 'up' | 'down') => {
        error = '';
        const pts = direction === 'up' ? 0.5 : -0.5;
        adjustmentPoints += pts;

        const formData = new FormData();
        formData.set('adjustment_points', String(pts));
        formData.set('team_id', String(entry.team_id));

        const response = await fetch(`/host/${$page.params.joincode}/leaderboard?/updatepointsadjustment`, {
            method: 'post',
            body: formData
        });

        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            error = result.data?.error as string;
            adjustmentPoints = entry.points_adjustment_value;
        }
    };

    const handleSetAdjustmentReason = async (e: Event) => {
        error = '';
        const target = e.target as HTMLSelectElement;
        const formData = new FormData();
        formData.set(target.name, target.value);
        formData.set('team_id', String(entry.team_id));

        const response = await fetch(`/host/${$page.params.joincode}/leaderboard?/updatepointsadjustment`, {
            method: 'post',
            body: formData
        });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            adjustmentReason = entry.points_adjustment_reason_id;
            error = result.data?.error as string;
        }
    };
</script>

<div class="points-adjustment-container">
    <p class="grow">Points Adjustment</p>
    <button class="plus-minus" id="minus-btn" on:click={() => handleSetAdjustmentPoints('down')}>-</button>
    <p>{adjustmentPoints}</p>
    <button class="plus-minus last" id="plus-btn" on:click={() => handleSetAdjustmentPoints('up')}>+</button>
</div>

{#if error}
    <p class="error" style:align-self="center">{error}</p>
{/if}

<div class="points-adjustment-container adjustment-reason">
    <p class="grow">Reason:</p>
    <select
        name="adjustment_reason"
        id="adjustment_reason"
        bind:value={adjustmentReason}
        on:input={handleSetAdjustmentReason}
    >
        {#each adjustmentReasons as reason}
            <option value={reason.id}>{reason.text}</option>
        {/each}
    </select>
</div>

<div class="points-adjustment-container">
    <p class="grow">Total Points</p>
    <p>{entry.total_points}</p>
</div>

<style lang="scss">
    .points-adjustment-container {
        display: flex;
        align-items: center;
        padding: 0 2rem;
        .plus-minus {
            font-size: 3.5rem;
            padding: 0 1rem;
            margin: 0;
        }
        .last {
            padding-right: 0;
        }
        select {
            width: 12rem;
            padding: 0.25rem;
            font-size: 1rem;
        }
    }
    .adjustment-reason {
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        margin: 0 1.75rem;
        padding: 0 0.25rem;
    }
    .error {
        width: 100%;
        text-align: center;
        color: var(--color-primary);
    }
</style>
