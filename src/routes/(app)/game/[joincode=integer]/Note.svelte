<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import NoteIcon from '$lib/icons/NoteIcon.svelte';

    const form = $page.form;

    const activeEventData = getStore('activeEventData');
    const questions = getStore('questions');
    $: activeQuestion = $questions.find((q) => q.key === $activeEventData.activeQuestionKey);

    const notes = getStore('teamNotes');
    $: activeQuestionNotes = $notes?.filter((n) => n.question_id === activeQuestion?.id) || [];

    let hidden = true;
</script>

<div id="notes-container" class="notes-container flex-column">
    {#if form?.error}<p>{form.error}</p>{/if}

    <button class="button disabled flex-column" on:click={() => (hidden = !hidden)}>
        <NoteIcon />
        <small>Click to {hidden ? 'Show' : 'Hide'} Notes</small>
    </button>
    {#key hidden}
        <form transition:slide|local={{ duration: 200 }} class:hidden action="?/submitnote" method="post" use:enhance>
            {#each activeQuestionNotes as note}
                <p class="note-text">{note.text}</p>
                <small class="note-meta">{note.user} {note.time}</small>
            {/each}
            <div id="note-container" class="input-container">
                <input type="hidden" name="question_id" value={activeQuestion?.id} />
                <input name="note_text" type="text" id="note-id" required />
                <label for="note-id">Add a New Note</label>
            </div>
        </form>
    {/key}
</div>

<style lang="scss">
    .hidden {
        display: none;
    }
    .button {
        padding: 0.5rem;
    }
    .note-text {
        margin: 1rem 1rem 0;
    }
    .note-meta {
        text-align: center;
    }
    .input-container {
        width: calc(100% - 2rem);
        margin-left: 1rem;
        input {
            width: 100%;
        }
    }
    small {
        font-weight: normal;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
    @media (max-width: 700px) {
        form {
            width: 100%;
        }
        label {
            width: calc(100% - 2rem);
        }
        // .input-container {
        //     width: 100%;
        // }
    }
</style>
