<script lang="ts">
    export let activeRoundQuestion: string;
    let hidden = true;
</script>

<div class="notes-container flex-column">
    <button class="button disabled" on:click={() => (hidden = !hidden)}>
        Notes for {activeRoundQuestion}
    </button>

    <form class:hidden on:submit|preventDefault>
        <div class="input-element">
            <input name="note" type="text" />
            <label for="note">Add a New Note</label>
        </div>
    </form>
</div>

<style lang="scss">
    .notes-container {
        background-color: #f2f2f2;
        max-width: calc(100% - 2em);
        margin-bottom: 1em;
        form {
            margin: auto;
        }
    }
    .disabled {
        background-color: inherit;
        &:focus {
            border: none;
        }
    }
    .hidden {
        display: none;
    }
</style>
