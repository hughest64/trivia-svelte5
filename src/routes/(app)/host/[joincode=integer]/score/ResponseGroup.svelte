<script lang="ts">
    import { getStore } from '$lib/utils';
    import Funny from '$lib/icons/Funny.svelte';
    import NotFunny from '$lib/icons/NotFunny.svelte';
    import Correct from '$lib/icons/Correct.svelte';
    import HalfCredit from '$lib/icons/HalfCredit.svelte';
    import Wrong from '$lib/icons/Wrong.svelte';
    import type { SvelteComponent } from 'svelte';
    import type { HostResponse } from '$lib/types';

    export let response: HostResponse;
    const activeEventData = getStore('activeEventData');

    let updating = false;
    const answerValueMap: Record<string, typeof SvelteComponent> = {
        '0': Wrong,
        '0.5': HalfCredit,
        '1': Correct
    };
    $: funnyIcon = response.funny ? Funny : NotFunny;

    const setScore = () => {
        const score = response.points_awarded;
        const newScore = score === 0 ? 0.5 : score === 1 ? 0 : 1;
        response.points_awarded = newScore;
        return newScore;
    };

    const updateResponse = async (type: string) => {
        updating = true;
        const data = new FormData();
        const funny = (response.funny = type === 'funny' ? !response.funny : response.funny);
        const points = type === 'points' ? setScore() : response.points_awarded;
        data.set('funny', String(funny));
        data.set('points_awarded', String(points));
        data.set('response_ids', JSON.stringify(response.response_ids));
        data.set('question_key', $activeEventData.activeQuestionKey);

        const updateResponse = await fetch('?/updateresponse', {
            method: 'post',
            body: data
        });
        // TODO: handle error properly
        if (!updateResponse.ok) {
            // revert
        }
        updating = false;
    };
</script>

<li class="scoring-response">
    <button type="submit" class="funny-button" class:updating on:click={() => updateResponse('funny')}>
        <svelte:component this={funnyIcon} />
    </button>
    <div class="scoring-details" class:updating>
        <p>{response.recorded_answer}</p>
        <button type="submit" class="score-icon" on:click={() => updateResponse('points')}>
            <svelte:component this={answerValueMap[String(response.points_awarded)]} />
            <p>{response.points_awarded} pts</p>
        </button>
    </div>
</li>
