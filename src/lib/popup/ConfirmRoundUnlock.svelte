<script lang="ts">
    import '$lib/styles/popup.scss';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';

    const popupData = getStore('popupData');
    const roundNumber = $popupData.data?.roundNumber;

    // TODO: this should be imported form a reusable place, or have a default on the Popup container
    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
    const unlock = async () => {
        const data = new FormData();
        data.set('round_number', roundNumber);
        data.set('locked', 'false');

        const response = await fetch('?/lock', { method: 'post', body: data });
        if (response.ok) {
            resetPopup();
        } else {
            console.log('TODO: handle the error');
        }
    };
</script>

<div class="pop-timer" />
<div class="pop-content">
    <h4>Confirm Round Unlock</h4>
    <p>Your Are about to unlock round {roundNumber}. Please confirm using the button below.</p>
    <button class="button button-primary" on:click={unlock}>Unlock it!</button>
</div>

<CloseButton on:click={resetPopup} />

<style lang="scss">
    .pop-content {
        padding-top: 0.75em;
    }
    button {
        align-self: center;
    }
</style>
