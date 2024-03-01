<script lang="ts">
    import { fly } from 'svelte/transition';
    import QuestionReveal from './QuestionReveal.svelte';
    import ConfirmRoundUnlock from './ConfirmRoundUnlock.svelte';
    import FinishGame from './FinishGame.svelte';
    import MegaroundReminder from './MegaroundReminder.svelte';
    import ImageroundReminder from './ImageroundReminder.svelte';
    import LeaderboardUpdate from './LeaderboardUpdate.svelte';
    import { getStore } from '$lib/utils';
    import type { ComponentType } from 'svelte';

    const popupData = getStore('popupData');

    const components: Record<string, ComponentType> = {
        question_reveal: QuestionReveal,
        round_unlock: ConfirmRoundUnlock,
        finish_game: FinishGame,
        megaround: MegaroundReminder,
        imageround: ImageroundReminder,
        leaderboard_update: LeaderboardUpdate
    };
</script>

{#if $popupData.is_displayed}
    <div class="pop-parent" transition:fly={{ y: -200, duration: 800 }}>
        <div class="pop">
            <svelte:component this={components[$popupData.popup_type]} />
        </div>
    </div>
{/if}
