<script lang="ts">
    import { getStore } from './utils';
    import { deserialize } from '$app/forms';
    const userData = getStore('userData');

    $: autoRevealValue = !!$userData?.auto_reveal_questions;

    let formError = '';
    const handleAutoReveal = async (e: Event) => {
        formError = '';
        const target = e.target as HTMLFormElement;

        userData.update((data) => ({ ...data, auto_reveal_questions: !data.auto_reveal_questions }));

        const formData = new FormData();
        formData.set('auto_reveal', String(!autoRevealValue));

        const response = await fetch(target.action, {
            method: 'post',
            body: formData
        });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            formError = result.data?.error as string;
            userData.update((data) => ({ ...data, auto_reveal_questions: !data.auto_reveal_questions }));
        }
    };
</script>

<form action="/user/settings?/auto_reveal_update" method="post" on:submit|preventDefault={handleAutoReveal}>
    <label class="switch">
        <input type="checkbox" bind:checked={autoRevealValue} />
        <button class="slider round" />
    </label>
</form>

<style lang="scss">
    form {
        flex-direction: row;
        justify-content: flex-end;
    }
    .switch {
        .slider {
            background-color: var(--color-secondary);
        }
        input:checked + .slider {
            background-color: var(--color-current);
        }
    }
</style>
