<script lang="ts">
    import '$lib/styles/popup.scss';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';

    const popupData = getStore('popupData');
    const winners = $popupData.data?.winners;
    const winnerText = winners.length > 1 ? 'And the Winners are...' : 'And the Winner is...';

    // TODO: this should be imported form a reusable place, or have a default on the Popup container
    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
</script>

<div class="pop-timer" />
<div class="pop-content">
    <h3>{winnerText}</h3>
    <h3>{winners.join(',')}</h3>
    <a href="https://www.triviamafia.com/schedule" rel="external" target="_blank">
        Check out our schedule for more Trivia
    </a>
</div>

<CloseButton on:click={resetPopup} />

<style lang="scss">
    .pop-content {
        padding-top: 0.75em;
        & * {
            padding: 0.25rem;
        }
    }
</style>
