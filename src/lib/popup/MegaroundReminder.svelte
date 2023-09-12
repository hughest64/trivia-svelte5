<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';

    const popupData = getStore('popupData');
    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
</script>

<div class="pop-timer" />
<div class="pop-content">
    <h3>Reminder!</h3>
    <h3>Remember to submit your Megaround!</h3>
    <a href="/game/{$page.params.joincode}/megaround" on:click={resetPopup}> Go to the Megaround </a>
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
