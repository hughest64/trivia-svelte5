<script lang="ts">
    import { activeRoundNumber, activeQuestionNumber } from '$stores/event'
    let hidden = true;
</script>

<div class="notes-container flex-column">
    <button
        class="button disabled"
        on:click={() => hidden = !hidden}
    >
        Notes for {$activeRoundNumber}.{$activeQuestionNumber}
    </button>
    <form class:hidden on:click|preventDefault>
        <div class="input-element">
            <input name="note" type="text" >
            <label for="note">Add a New Note</label>
        </div>
    </form>
</div>

<style lang="scss">
    .notes-container {
		// width: 100%;
		display: inline-flex;
		flex-direction: column;
        background-color: #f2f2f2;
        form {
            margin: auto;
        }
	}
    .disabled {
        background-color: inherit;
    }
    .hidden {
        display: none;
    }
</style>