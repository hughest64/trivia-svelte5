<script lang="ts">
    import { page } from '$app/stores';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;

    const adjustmentReasons = $page.data.points_adjustment_reasons || [];

    let adjustmentReason = entry.points_adjustment_reason_id;
    let adjustmentPoints = entry.points_adjustment_value;

    const handleSetAdjustmentPoints = async (direction: 'up' | 'down') => {
        const pts = direction === 'up' ? 0.5 : -0.5;
        adjustmentPoints += pts;

        const formData = new FormData();
        formData.set('adjustment_points', String(pts));
        formData.set('team_id', String(entry.team_id));

        const response = await fetch('?/updatepointsadjustment', {
            method: 'post',
            body: formData
        });
        if (!response.ok) {
            // reset the points
            // show an error msg
        }
    };

    const handleSetAdjustmentReason = async (e: Event) => {
        const target = e.target as HTMLSelectElement;
        const formData = new FormData();
        formData.set(target.name, target.value);
        formData.set('team_id', String(entry.team_id));

        const response = await fetch('?/updatepointsadjustment', {
            method: 'post',
            body: formData
        });
        if (!response.ok) {
            // reset the selected value
            // show an error msg
        }
    };
</script>

<div class="points-adjustment-container">
    <p class="grow">Points Adjustment</p>
    <button class="plus-minus" on:click={() => handleSetAdjustmentPoints('down')}>-</button>
    <p>{adjustmentPoints}</p>
    <button class="plus-minus last" on:click={() => handleSetAdjustmentPoints('up')}>+</button>
</div>

<!-- TODO: if adjustmentPoints !== 0 -->
<div class="points-adjustment-container adjustment-reason">
    <p class="grow">Reason:</p>
    <select
        name="adjustment_reason"
        id="adjustment_reason"
        bind:value={entry.points_adjustment_reason_id}
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
</style>
