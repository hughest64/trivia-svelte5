<script lang="ts">
    import '$lib/styles/popup.scss';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';
    import type { PopupData } from '$lib/types';

    $: popupData = getStore<PopupData>('popupData');

    // TODO: this should be import form a reusable place, or have a default on the Popup container
    const resetPopup = () => $popupData = { is_displayed: false, popup_type: '' };
   
</script>
<!-- TODO: get fancy w/ css so we don't need this div -->
<div class="pop-timer">
    <h4>{''}</h4>
</div>
<div class="pop-content">
    <h4>Conform Round Unlock</h4>
    <p>Your Are about to unlock round X. Please confirm using the button below.</p>
    <button class="button">Unlock it!</button>
</div>

<CloseButton on:click={resetPopup} />