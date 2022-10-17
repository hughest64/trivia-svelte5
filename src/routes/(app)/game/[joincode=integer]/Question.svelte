<script lang="ts">
    import { page } from '$app/stores';
    import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
    import type { EventQuestion, Response } from '$lib/types';

    export let error = '';
    export let activeRoundQuestion: string;
    export let activeQuestion: EventQuestion;
    export let activeResponse: Response | undefined;
    $: responseText = activeResponse?.recorded_answer || '';

    $: userData = $page.data?.user_data;
    $: response = responseText;
    $: notsubmitted = response && activeResponse?.recorded_answer !== response;

    const handleResponse = async () => {
        console.log($page.data.fetchHeaders.cookie);
        const postResponse = await fetch(
            `${apiHost}/game/${$page.params.joincode}/response/${activeResponse?.id || 'create'}`,
            {
                method: 'POST',
                credentials: 'include',
                headers: $page.data.fetchHeaders,
                body: JSON.stringify({
                    response_text: response,
                    key: activeRoundQuestion,
                    team_id: userData?.active_team_id
                })
            }
        );

        if (!postResponse.ok) {
            error = (await postResponse.json()).detail;
        }
    };
</script>

<h2>{activeRoundQuestion}</h2>

<p class="question-text">{activeQuestion.text}</p>

<form on:submit|preventDefault={handleResponse}>
    
    <div class="input-element" class:notsubmitted>
        <input required name="response_text" type="text" bind:value={response} on:change={() => (error = '')} />
        <label for="response_text">Enter Answer</label>
    </div>
    
    {#if error}<p>{error}</p>{/if}

    <button class="button button-red">Submit</button>
</form>

<style lang="scss">
    h2 {
        margin: 0.5em;
    }

    .question-text {
        padding: 0 1em;
    }

    .notsubmitted {
        input {
            border-color: var(--color-red);
        }
        label {
            background-color: var(--color-red);
        }
    }
</style>
