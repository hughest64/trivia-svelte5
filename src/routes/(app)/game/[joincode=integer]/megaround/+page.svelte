<script lang="ts">
    import { getStore } from '$lib/utils';

    const questions = getStore('questions');
    const rounds = getStore('rounds');
    const responses = getStore('responseData');

    let selectedRoundNumber = 5; // : number;
    $: roundQuestions = $questions.filter((q) => q.round_number === selectedRoundNumber);

    const roundNumbers = $rounds?.map((rd) => rd.round_number) || [];
    const defaultText = 'You Have not answered this question!';

    const handleRoundSelect = (event: MouseEvent) => {
        const roundNum = (event.target as HTMLElement).id;
        selectedRoundNumber = Number(roundNum);
    };
</script>

<h1>Mega Round</h1>
<small>
    <strong>Instructions: </strong>
    Choose one Mega Round. Then weight each answer 1-5, using each number once. 5 = your most confident answer, 1 = least
    confident.
</small>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        {#if roundNum > roundNumbers.length / 2}
            <button class:active={selectedRoundNumber === roundNum} id={String(roundNum)} on:click={handleRoundSelect}>
                {roundNum}
            </button>
        {/if}
    {/each}
</div>

<!-- form for selected mr, no inputs show up if no mr is selected, answers show for resps on the selected mr -->
<!-- keyboard is disabled, must use -->

{#if selectedRoundNumber}
    <form action="">
        {#each roundQuestions as question (question.id)}
            <div class="input-container">
                <input
                    type="tel"
                    min="1"
                    max="5"
                    class="megaround-weight"
                    id="megaround-weight-{question.question_number}"
                    name="megaround-weight-{question.question_number}"
                />
                <p>{$responses.find((r) => r.key === question.key)?.recorded_answer || defaultText}</p>
            </div>
        {/each}

        <div class="megaround-weight-selector">
            {#each [1, 2, 3, 4, 5] as num}
                <button id="megaround-value-{num}" class="button-white">{num}</button>
            {/each}
        </div>

        <!-- submit button (disabled until all fields are filled in), need validation that all values are unique-->
        <button type="submit" class="button button-primary">Submit</button>
        <button class="button button-secondary">Clear & Edit</button>
    </form>
{/if}

<style lang="scss">
    small {
        font-size: 16px;
    }
    .round-selector {
        margin: 1rem 0;
    }
    form {
        .input-container {
            display: flex;
            align-items: center;
            margin: 0.25rem 0;
            padding: 0;
            column-gap: 0.25rem;
            p {
                font-size: 1rem;
                margin: 0;
            }
        }
        input {
            width: 40px;
            height: 40px;
            border: 2px solid var(--color-secondary);
            border-radius: 5px;
            margin: 0;
            margin-right: 0.25rem;
            padding: 0;
            text-align: center;
        }
    }
    .megaround-weight-selector {
        display: flex;
        align-self: center;
        gap: 1rem;
        margin: 1rem 0;
        button {
            width: 3rem;
            height: 3rem;
            font-weight: bold;
            font-size: 1.25rem;
            border: 2px solid var(--color-secondary);
            border-radius: 50%;
            cursor: pointer;
        }
    }
</style>
