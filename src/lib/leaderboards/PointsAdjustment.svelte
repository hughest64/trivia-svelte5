<script lang="ts">
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;

    let adjustmentPoints = 0;
</script>

<div class="points-adjustment-container">
    <p class="grow">Points Adjustment</p>
    <button class="plus-minus">-</button>
    <p>{adjustmentPoints}</p>
    <button class="plus-minus last">+</button>
</div>

<div class="points-adjustment-container adjustment-reason">
    <p class="grow">Reason:</p>
    <select name="ajustment_reason" id="ajustment_reason">
        <option value="-">----</option>
        <option value="a">A</option>
        <option value="b">B</option>
        <option value="c">C</option>
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
            width: 10rem;
            padding: 0.25rem;
            font-size: 1rem;
            // border-radius: 5px;
        }
    }
    .adjustment-reason {
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        margin: 0 1.75rem;

        padding: 0 0.25rem;
    }
</style>
