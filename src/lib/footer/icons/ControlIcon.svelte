<script lang="ts">
    export let cls: string = '';
</script>

<svg width="41" height="47" viewBox="0 0 41 47" fill="none" xmlns="http://www.w3.org/2000/svg" class={cls}>
    <rect x="4" width="4.5" height="47" rx="2.5" />
    <rect x="18" width="4.55" height="47" rx="2.5" />
    <rect x="32" width="4.55" height="47" rx="2.5" />
    <circle cx="6.5" cy="24.5" r="5.5" />
    <circle cx="20.5" cy="34.5" r="5.5" />
    <circle cx="34.5" cy="15.5" r="5.5" />
</svg>

<style lang="scss">
    rect,
    circle {
        fill: var(--color-alt-black);
    }
</style>
