<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    const questions = getStore('questions');
    const key = $page.url.searchParams.get('key');

    const source = $questions.find((q) => q.key === key)?.question_url;
</script>

<div class="lightbox">
    <div class="image-container">
        <img src={source} alt="" />
    </div>
    <button on:click={() => window.history.back()}>Close Image</button>
</div>

<style lang="scss">
    .lightbox {
        position: fixed;
        top: 0;
        z-index: 98;
        height: 100vh;
        width: 100%;
        max-width: var(--max-container-width);
        background: rgba(0, 0, 0, 0.75);
        display: flex;
        flex-direction: column;
    }

    .image-container {
        height: calc(100% - 4rem);
        width: 100%;

        img {
            background-color: rgba(0, 0, 0, 0.75);
            // background-color: #fcfcfc;
            object-fit: contain;
            width: 100%;
            height: 100%;
        }
    }

    button {
        color: #fcfcfc;
        display: block;
        width: 100%;
        max-width: var(--max-container-width);
        background: rgba(0, 0, 0, 0.75);
        margin: 0;
        padding: 1rem 0;
        text-align: center;
    }
</style>
