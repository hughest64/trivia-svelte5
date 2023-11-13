<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';

    const popupData = getStore('popupData');
    $: count = $popupData.timer_value || 5;
    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
    let interval: ReturnType<typeof setTimeout>;
    const countDown = () => {
        if (count > 0) {
            count--;
            setTimeout(countDown, 1000);
        } else {
            clearTimeout(interval);
            resetPopup();
        }
    };

    $: setTimeout(countDown, 1000);
</script>

<div class="pop-timer" />
<div class="pop-content">
    <h3>Leaderboard Update</h3>
    <h3>The leaderboard has been updated!</h3>
    <a href="/game/{$page.params.joincode}/leaderboard" on:click={resetPopup}> Check it out </a>
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
