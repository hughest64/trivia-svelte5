<script lang="ts">
    import '$lib/styles/popup.scss';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';
    import type { PopupData } from '$lib/types';

    $: popupData = getStore<PopupData>('popupData');
    $: roundNumber = $popupData.data?.roundNumber;

    // TODO: this should be import form a reusable place, or have a default on the Popup container
    const resetPopup = () => $popupData = { is_displayed: false, popup_type: '' };
    const unlock = () => $popupData = { is_displayed: false, popup_type: '', data: { unlock: roundNumber } };
   
</script>

<div class="pop-timer"></div>
<div class="pop-content">
    <h4>Confirm Round Unlock</h4>
    <p>Your Are about to unlock round {roundNumber}. Please confirm using the button below.</p>
    <button class="button button-red" on:click={unlock}>Unlock it!</button>
</div>

<CloseButton on:click={resetPopup} />

<style lang="scss">
    .pop-content {
        padding-top: .75em;
    }
</style>